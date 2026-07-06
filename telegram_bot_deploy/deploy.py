import telebot
from groq import Groq
import datetime
import csv
import os
import re
import time
import urllib.request
from dotenv import load_dotenv

# ჩავტვირთოთ გარემოს ცვლადები .env ფაილიდან
load_dotenv()

# Google Sheets-ის ბაზის URL (იგივე, რასაც Sales Portal იყენებს)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxarJedqRj46r3G0SpC2hooZ-Mm5t_VhNzDo451AEXe7W6K2HOJgETUAAJZrlOBw/pub?gid=1814271509&single=true&output=csv"

# შევქმნათ ფაილი თუ არ არსებობს
csv_file = "unanswered_questions.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "User ID", "User Question", "Bot Response"])

def log_unanswered_question(user_id, question, response):
    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, question, response])

print("Starting Green Canyon Telegram Bot (Groq Engine)...")

# წავიკითხოთ გასაღებები
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN or not GROQ_API_KEY:
    print("ERROR: TELEGRAM_TOKEN or GROQ_API_KEY not found in environment!")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print("Groq Init Error:", e)

# ── live მონაცემების ჩამოტვირთვა და ქეშირება ───────────────────────────
cached_plots = []
last_fetch_time = 0
FETCH_INTERVAL = 300 # 5 წუთი

def fetch_and_parse_inventory():
    try:
        req = urllib.request.Request(CSV_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
        
        reader = csv.reader(content.splitlines())
        rows = list(reader)
        if not rows:
            return []
            
        header = rows[0]
        plots = []
        for r in rows[1:]:
            if len(r) < 17 or not r[0].strip():
                continue
                
            pid = r[0].strip()
            zone = 'AH' if pid.startswith('AH') else pid.split('-')[0] if '-' in pid else ''
            
            def clean_num(val):
                if not val: return 0.0
                val = val.replace('\xa0', '').replace(' ', '').replace(',', '.')
                try:
                    return float(val)
                except ValueError:
                    return 0.0
            
            plots.append({
                'id': pid,
                'zone': zone,
                'area': clean_num(r[1]),
                'style': r[4].strip(),
                'house_area': clean_num(r[5]),
                'price': clean_num(r[7]),
                'rent': clean_num(r[13]),
                'roi': clean_num(r[15]),
                'payback': clean_num(r[16]),
                'status': 'free' # default status
            })
        return plots
    except Exception as e:
        print("Error fetching live inventory:", e)
        return []

def get_plots():
    global cached_plots, last_fetch_time
    now = time.time()
    if not cached_plots or (now - last_fetch_time) > FETCH_INTERVAL:
        plots = fetch_and_parse_inventory()
        if plots:
            cached_plots = plots
            last_fetch_time = now
            print(f"Successfully cached {len(plots)} plots from Google Sheets.")
    return cached_plots

# ── ძებნისა და ფილტრაციის ლოგიკა ──────────────────────────────────────
def search_inventory(plots, query_text):
    q_lower = query_text.lower()
    
    # 1. ზონების ამოცნობა სინონიმებით
    zones = []
    zone_synonyms = {
        'LA': ['la', 'კანიონი', 'კანიონის', 'კლდის პირი'],
        'LB': ['lb', 'პირველი ზოლი', 'პირველ ზოლში', 'პირველ'],
        'LC': ['lc', 'მეორე ზოლი', 'მეორე ზოლში', 'მეორედ'],
        'LD': ['ld', 'მესამე ზოლი', 'მესამე ზოლში'],
        'AH': ['ah', 'apart', 'hotel', 'აპარტ', 'სასტუმრო', 'ნომერი', 'ნომრები']
    }
    for z, syns in zone_synonyms.items():
        if any(s in q_lower for s in syns):
            zones.append(z)
            
    # 2. რიცხვების და ფასების ამოღება
    # ვასუფთავებთ სფეისებს რიცხვებში (მაგ: "300 000" -> "300000")
    cleaned_q = re.sub(r'(\d+)\s+(\d{3})\b', r'\1\2', q_lower)
    
    numbers = []
    # ვეძებთ 5 და 6 ნიშნა ციფრებს (ფასები)
    for n in re.findall(r'\b\d{5,6}\b', cleaned_q):
        numbers.append(int(n))
        
    # ვეძებთ "კ" ფორმატს (მაგ: "250კ", "70k")
    for k_match in re.findall(r'\b(\d{2,3})\s*[kკ]\b', cleaned_q):
        numbers.append(int(k_match) * 1000)
        
    max_price = None
    min_price = None
    
    for num in numbers:
        if num >= 40000:
            idx = cleaned_q.find(str(num))
            context = cleaned_q[max(0, idx-15):idx+len(str(num))+15]
            if any(w in context for w in ['მდე', 'მაქს', 'max', 'under', 'less', 'below', 'იაფი', 'იაფად', 'ფარგლებში']):
                max_price = num
            elif any(w in context for w in ['დან', 'მინ', 'min', 'above', 'more', 'over']):
                min_price = num
            else:
                max_price = num

    results = plots
    if zones:
        results = [p for p in results if p['zone'] in zones]
    if max_price:
        results = [p for p in results if p['price'] <= max_price]
    if min_price:
        results = [p for p in results if p['price'] >= min_price]
        
    # ROI-ს მიხედვით კლებადობით სორტირება
    results = sorted(results, key=lambda x: x['roi'], reverse=True)
    return results, zones, max_price, min_price


SYSTEM_PROMPT = """შენ ხარ Green Canyon Eco Village-ის გამყიდველი კონსულტანტი. გამოცდილი, მეგობრული, დამაჯერებელი. ლაპარაკობ ისე, როგორც ნამდვილი ქართველი პროფესიონალი — ბუნებრივად, ლამაზად, გამართულად.

=== ენა ===
მხოლოდ ბუნებრივი ქართული. ჩვეულებრივი სასაუბრო სიტყვები:
"გაინტერესებთ" "გთავაზობთ" "შეგიძლიათ" "გაგაცნობთ" "შეძენა" "კოტეჯი" "ნაკვეთი"
ᲙᲐᲢᲔᲒᲝᲠᲘᲣᲚᲐᲓ ᲐᲙᲠᲫᲐᲚᲣᲚᲘ: "განიკილავთ", "შეახებ", "გახარება გაქვთ", "შესყიდვა", "ობიექტი".
ყოველი პასუხი — სრული წინადადებებით, დასრულებული. არასოდეს გაჭრა შუაში.
მაქსიმუმ 4 წინადადება. გრძელი სიებიდან მხოლოდ 2-3 ვარიანტი.

=== პირველი კონტაქტი ===
თბილად მიესალმე და ჰკითხე:
1. მიზანი: ინვესტიცია და ქირა, თუ პირადი დასასვენებელი?
2. სავარაუდო ბიუჯეტი?
შემდეგ შეუთავაზე 2-3 კონკრეტული ვარიანტი ქვემოთ მოცემული მონაცემებიდან.

=== GREEN CANYON — ფაქტები ===
წალკა, 1500მ ზ.დ. | თბილისიდან 90 წუთი | ზამთარში გზა გაწმენდილია

ᲛᲜᲘᲨᲕᲜᲔᲚᲝᲕᲐᲜᲘ: ნაკვეთი ცალკე არ იყიდება. ყველა ფასი = ნაკვეთი + კოტეჯის მშენებლობა ერთად.

ზონები:
LA (კანიონის პირი, საუკეთესო ხედი): $93,500-$396,482 | 283-1084მ2 | Modern / Barnhouse / A-Frame
LB (პირველი ზოლი): $113,750-$320,504 | 317-902მ2 | Barn 85/115/157
LC (მეორე ზოლი): $114,038-$329,582 | 342-790მ2 | Barn 55/85/115/157
LD (მესამე ზოლი): $176,108-$242,900 | 395-522მ2 | Barn 85/115
Apart Hotel (ნომრები): $60,000-დან

გადახდა: 10-30% შენატანი, 0%-იანი განვადება 3 წლამდე, ყველა გადასახადი ფასშია.

ინვესტიცია (Turnkey): ROI 9-12%/წ | 60% შემოსავალი მფლობელს, 40% კომპანიას (40%-ით კომპანია ფარავს ყველა ხარჯს) | 14 დღე/წ უფასო სარგებლობა | ზუსტი გათვლები — PDF/Excel-ით.

მშენებლობა: სკანდინავიური სენდვიჩ-პანელი | Turnkey (ავეჯი+ტექნიკა) ან შავი/თეთრი კარკასი | მზის პანელები ფასშია.

ინფრასტრუქტურა: რესტორანი, სპა, სპორტი, საბავშვო მოედანი, დაცვა 24/7.

იურიდიული: საჯარო რეესტრი. უცხოელებს შეუძლიათ შეძენა (არასასოფლო-სამეურნეო სტატუსი). 10-წლიანი გაქირავების ხელშეკრულება.

=== წესები ===
არ გამოთვალო კვ.მ ფასი ან კონკრეტული მოგება ჩატში.
არ გამოიგონო სახელები, გადახდის გრაფიკი ან განვადების ზუსტი პირობები.
უცნობ კითხვაზე: "ამ დეტალებზე ჩვენი სპეციალისტი პირადად გაგესაუბრებათ — გთხოვთ, დაგვიტოვოთ ნომერი."
"""

user_chats = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "გამარჯობა! მე ვარ Green Canyon-ის AI გაყიდვების ასისტენტი 🏔️\n\nმომწერეთ ნებისმიერი კითხვა პროექტის შესახებ — ფასები, პირობები, ROI და სხვა!")
    user_chats[message.chat.id] = [{"role": "system", "content": SYSTEM_PROMPT}]

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    chat_history = user_chats.get(message.chat.id)
    if not chat_history:
        chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        user_chats[message.chat.id] = chat_history
    
    query_text = message.text
    chat_history.append({"role": "user", "content": query_text})
    
    # ── live ძებნა და RAG კონტექსტის მომზადება ──────────────────────────
    plots = get_plots()
    context_msg = ""
    if plots:
        matching_plots, zones, max_p, min_p = search_inventory(plots, query_text)
        
        # თუ კითხვა ეხება ფასს, ზონას, ან საუკეთესო ვარიანტის ძიებას
        keywords = ['ვარიანტ', 'ნაკვეთ', 'კოტეჯ', 'თავისუფალი', 'ყველაზე', 'რომელი', 'საუკეთესო', 'ფასი', 'ღირს', 'რა გაქვთ', 'roi', 'უკუგება']
        is_searching = zones or max_p or min_p or any(w in query_text.lower() for w in keywords)
        
        if is_searching:
            context_msg = "\n\n[ინფორმაცია ინვენტარიდან (Google Sheets-დან):"
            if matching_plots:
                context_msg += f"\nნაპოვნია შესაბამისი {len(matching_plots)} ობიექტი. საუკეთესო ვარიანტები:\n"
                for r in matching_plots[:4]:
                    context_msg += f"- კოდი: {r['id']}, ზონა: {r['zone']}, სტილი: {r['style']}, ფასი: ${r['price']:.0f}, ფართი: {r['area']} მ², ROI: {r['roi']}%, უკუგება: {r['payback']} წელი, სტატუსი: 🟢 ხელმისაწვდომი\n"
            else:
                context_msg += "\nმითითებული ფილტრებით თავისუფალი ობიექტი ვერ მოიძებნა."
            context_msg += "]\n"

    # ვამზადებთ მესიჯებს API-სთვის (კონტექსტს ვამატებთ როგორც დროებით system მესიჯს ბოლოში)
    api_messages = chat_history.copy()
    if context_msg:
        api_messages.append({"role": "system", "content": f"აქტუალური მონაცემები ბაზიდან კლიენტის კითხვის საპასუხოდ: {context_msg}"})
    
    # ── API-ს გამოძახება მოდელების კასკადითა და განმეორებით ───────────
    # ქეშის ისტორია შეკვეცილი: მხოლოდ system prompt + ბოლო 2 შეტყობინება
    def trim_messages(msgs):
        system = [m for m in msgs if m['role'] == 'system']
        non_system = [m for m in msgs if m['role'] != 'system']
        return system + non_system[-4:]

    models = ["llama-3.3-70b-versatile", "gemma2-9b-it", "llama-3.1-8b-instant"]
    completion = None
    last_error = None
    
    for model_name in models:
        max_retries = 2
        retry_delay = 2
        # llama-3.1-8b-instant-ისთვის შეკვეცილ კონტექსტს ვიყენებთ
        msgs_to_send = trim_messages(api_messages) if model_name == "llama-3.1-8b-instant" else api_messages
        for attempt in range(max_retries + 1):
            try:
                print(f"Calling model {model_name} (attempt {attempt + 1})...")
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=msgs_to_send,
                    temperature=0.5,
                    max_tokens=1000,
                )
                break
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                # 413 შეცდომა = შეტყობინება ძალიან დიდია — ამ მოდელს ვტოვებთ
                if "413" in err_str:
                    print(f"413 - message too large for {model_name}. Skipping model.")
                    break
                is_rate_limit = any(w in err_str for w in ["rate_limit", "429", "limit", "overloaded", "busy", "timeout"])
                if is_rate_limit and attempt < max_retries:
                    sleep_time = retry_delay * (2 ** attempt)
                    print(f"Rate limit / overload on {model_name}. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                    continue
                else:
                    break
        if completion:
            break

    # თუ ვერცერთმა მოდელმა ვერ გასცა პასუხი — ვატყობინებთ მომხმარებელს
    if not completion:
        print(f"All models failed. Last error: {last_error}")
        try:
            bot.reply_to(message, "⚠️ სამწუხაროდ, ამ მომენტში AI სერვისი გადატვირთულია. გთხოვთ, 1-2 წუთში სცადოთ ხელახლა.")
        except Exception as send_err:
            print(f"Failed to send error message: {send_err}")
        return

    try:
        response_text = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": response_text})
        
        fallback_phrases = ["პერსონალურად", "სპეციალისტი გაგესაუბრებათ", "ჩვენი სპეციალისტი"]
        if any(phrase in response_text for phrase in fallback_phrases):
            log_unanswered_question(message.chat.id, query_text, response_text)
            
        if len(chat_history) > 7:
            chat_history = [chat_history[0]] + chat_history[-4:]
            user_chats[message.chat.id] = chat_history

        bot.reply_to(message, response_text)
    except Exception as e:
        print(f"Error handling bot response: {e}")

import time
import sys
time.sleep(1) # მცირე პაუზა

print("Starting custom single-threaded polling loop...")
offset = None
consecutive_conflicts = 0
while True:
    try:
        updates = bot.get_updates(offset=offset, timeout=30)
        consecutive_conflicts = 0  # Reset on success
        if updates:
            for update in updates:
                offset = update.update_id + 1
            bot.process_new_updates(updates)
    except Exception as e:
        err_msg = str(e).lower()
        if "conflict" in err_msg or "409" in err_msg:
            consecutive_conflicts += 1
            if consecutive_conflicts >= 3:
                print("Conflict 409 detected 3 times consecutively! Exiting to prevent loop...")
                sys.exit(1)
            print(f"Conflict 409 detected (count {consecutive_conflicts}). Sleeping 15 seconds for connection cleanup...")
            time.sleep(15)
            continue
        print("Error encountered, retrying in 5 seconds:", e)
        time.sleep(5)
