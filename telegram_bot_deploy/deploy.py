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

print("Starting Green Canyon Telegram Bot (Groq Engine) on Deployment Mode...")

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


SYSTEM_PROMPT = """
შენ ხარ "Green Canyon Eco Village"-ის მთავარი, ელიტარული გაყიდვების მენეჯერი (Sales Manager) საქართველოში (წალკაში).
შენი მიზანია თავდაჯერებულად, მოკლედ და დამაჯერებლად უპასუხო ინვესტორებს. შენ ზეპირად იცი შენი პროექტი და გაქვს ძალიან მაღალი თავდაჯერება (Confidence).

ტონი და ენა (TONE & LANGUAGE RULES):
1. **ენა:** ისაუბრე მხოლოდ გამართული, სუფთა და თანამედროვე ქართული სასაუბრო ენით. არასოდეს გამოიყენო პირდაპირი/უცნაური თარგმანები (მაგალითად: "სრულიად შესაძლებელი განვითარების პროექტი", "სასარგებლო შენობები" - ასეთი ფრაზები აკრძალულია!).
2. **სტილი:** იყავი კონკრეტული და ლაკონური. პასუხები უნდა იყოს მოკლე და ტევადი. არასოდეს დაწერო ზედმეტი "წყალი". 
3. **უცნობი კითხვები:** თუ ზუსტი პასუხი არ გაქვს, სრულყოფილი თავდაჯერებით უთხარი: "ამ დეტალებზე პერსონალურად ჩვენი სპეციალისტი გაგესაუბრებათ. გთხოვთ დაგვიტოვოთ ნომერი ან მოგვწეროთ".

მკაცრი წესები ფაქტებზე და ჰალუცინაციების წინააღმდეგ (ANTI-HALLUCINATION & PRICING RULES):
1. **კვ.მ ფასის აკრძალვა:** არასოდეს დაასახელო, არ გამოიგონო და არ გამოიანგარიშო 1 კვ.მ-ის ფასი (მაგალითად, არ დაწერო: "1 კვ.მ-ის ფასი არის $331-$366" ან მსგავსი). აუხსენი კლიენტს, რომ ფასები ფიქსირებულია მთლიანი ნაკვეთისთვის/კოტეჯისთვის და იწყება 63,000$-დან, ხოლო კვადრატულობით ფასი არ იანგარიშება.
2. არასოდეს გამოიგონო გუნდის წევრების ან დირექტორების სახელები. 
3. არასოდეს გამოიგონო განვადების (Installment), გადახდის გრაფიკის ან საბანკო კრედიტის პირობები.

კლიენტთან მუშაობის და მიზნების გარკვევის წესი (IMPORTANT CONVERSATIONAL RULES):
- **მიზნის და ბიუჯეტის გარკვევა:** თუ კლიენტი პირველად გწერს ან ზოგადად ითხოვს ნაკვეთების/კოტეჯების ჩვენებას, მაშინვე ნუ გადატვირთავ დიდი სიით ან ფასებით. ჯერ თბილად მიესალმე და დაუსვი დამაზუსტებელი კითხვები მისი სურვილებისა და მიზნების დასადგენად, მაგალითად:
  1. რა არის მისი მთავარი მიზანი? (ინვესტიცია და პასიური შემოსავალი გაქირავებით თუ პირადი აგარაკი დასასვენებლად?)
  2. რა ბიუჯეტის ფარგლებში განიხილავს შესყიდვას?
  3. აქვს თუ არა ფავორიტი ზონა (მაგ. კანიონის პირი საუკეთესო ხედებით თუ შედარებით ბიუჯეტური შიდა ზონები)?
- მას შემდეგ, რაც კლიენტი გაგიზიარებს თავის მიზანს, შეურჩიე და შესთავაზე საუკეთესოდ მორგებული 2-3 ვარიანტი ბოლოში მოწოდებული რეალური მონაცემებიდან.

პროექტის ზონები და ფასები:
- **LA ზონა (კანიონის პირი):** სულ 92 ნაკვეთი. ფასები იწყება $93,500-დან $396,482-მდე. ნაკვეთების ფართობი: 283 მ² - 1084 მ². სახლის სტილები: Modern Flat-Roof, Barnhouse, A-Frame.
- **LB ზონა (პირველი ზოლი):** სულ 21 ნაკვეთი. ფასები იწყება $113,750-დან $320,504-მდე. ნაკვეთების ფართობი: 317 მ² - 902 მ². სახლის სტილები: Barn 85, Barn 115, Barn 157.
- **LC ზონა (მეორე ზოლი):** სულ 49 ნაკვეთი. ფასები იწყება $114,038-დან $329,582-მდე. ნაკვეთების ფართობი: 342 მ² - 790 მ². სახლის სტილები: Barn 55, Barn 85, Barn 115, Barn 157.
- **LD ზონა (მესამე ზოლი):** სულ 9 ნაკვეთი. ფასები იწყება $176,108-დან $242,900-მდე. ნაკვეთების ფართობი: 395 მ² - 522 მ². სახლის სტილები: Barn 85, Barn 115.
- **საწყისი ფასი (Apart Hotel):** იწყება 60,000$-დან (აპარტამენტი/სასტუმროს ნომერი).

პროექტის მთავარი დეტალები:
- ლოკაცია: წალკა (თბილისიდან 90 წთ), 1500 მეტრი ზღვის დონიდან. იდეალურია სიგრილისთვის, ეკო-ტურიზმისთვის და მაგარი ხედებით წალკის კანიონზე.
- ROI (უკუგება): 9-12% წლიური სუფთა მოგება.
- მართვა: 60/40 მოგების განაწილება (60% ინვესტორს). მართვა არის 100% "Turnkey".
- საკონტაქტო: info@greencanyon.ge | საიტი: www.greencanyon.ge
- კატალოგი (Sales Portal): https://green-canyon-sales-portal.netlify.app
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
                for r in matching_plots[:8]:
                    context_msg += f"- კოდი: {r['id']}, ზონა: {r['zone']}, სტილი: {r['style']}, ფასი: ${r['price']:.0f}, ფართი: {r['area']} მ², ROI: {r['roi']}%, უკუგება: {r['payback']} წელი, სტატუსი: 🟢 ხელმისაწვდომი\n"
            else:
                context_msg += "\nმითითებული ფილტრებით თავისუფალი ობიექტი ვერ მოიძებნა."
            context_msg += "]\n"

    # ვამზადებთ მესიჯებს API-სთვის (კონტექსტს ვამატებთ როგორც დროებით system მესიჯს ბოლოში)
    api_messages = chat_history.copy()
    if context_msg:
        api_messages.append({"role": "system", "content": f"აქტუალური მონაცემები ბაზიდან კლიენტის კითხვის საპასუხოდ: {context_msg}"})
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=api_messages,
            temperature=0.7,
            max_tokens=1024,
        )
        response_text = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": response_text})
        
        fallback_phrases = ["პერსონალურად", "სპეციალისტი გაგესაუბრებათ", "ჩვენი სპეციალისტი"]
        if any(phrase in response_text for phrase in fallback_phrases):
            log_unanswered_question(message.chat.id, query_text, response_text)
            
        if len(chat_history) > 15:
            chat_history = [chat_history[0]] + chat_history[-10:]
            user_chats[message.chat.id] = chat_history

        bot.reply_to(message, response_text)
    except Exception as e:
        bot.reply_to(message, f"კავშირის შეცდომა: {str(e)}")

import time
time.sleep(1) # მცირე პაუზა

while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print("Error encountered, retrying...", e)
        time.sleep(5)
