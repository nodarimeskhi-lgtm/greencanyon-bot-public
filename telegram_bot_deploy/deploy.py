import telebot
import google.generativeai as genai
from groq import Groq
import datetime
import csv
import os
import re
import time
import threading
import urllib.request
from dotenv import load_dotenv

load_dotenv()

CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSxarJedqRj46r3G0SpC2hooZ-Mm5t_VhNzDo451AEXe7W6K2HOJgETUAAJZrlOBw/pub?gid=1814271509&single=true&output=csv"

csv_file = "unanswered_questions.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "User ID", "User Question", "Bot Response"])

def log_unanswered_question(user_id, question, response):
    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, question, response])

print("Starting Green Canyon Telegram Bot (Gemini Engine)...")

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GROQ_API_KEY   = os.getenv('GROQ_API_KEY')

if not TELEGRAM_TOKEN:
    print("ERROR: TELEGRAM_TOKEN not found!")
    exit(1)
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found — will use Groq only!")

bot = telebot.TeleBot(TELEGRAM_TOKEN, threaded=True, num_threads=8)

# Gemini კლიენტი
gemini_model = None
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel("gemini-2.0-flash")
        print("Gemini 2.0 Flash initialized successfully.")
    except Exception as e:
        print(f"Gemini init error: {e}")

# Groq fallback
groq_client = None
if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("Groq fallback initialized.")
    except Exception as e:
        print(f"Groq init error: {e}")

# ── ინვენტარის ქეში ───────────────────────────────────────────────────────
cached_plots = []
last_fetch_time = 0
FETCH_INTERVAL = 300
cache_lock = threading.Lock()

def fetch_and_parse_inventory():
    try:
        req = urllib.request.Request(CSV_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')

        lines = content.strip().split('\n')
        reader = csv.DictReader(lines)
        plots = []
        for row in reader:
            try:
                price_str = row.get('Price', '0').replace('$', '').replace(',', '').strip()
                area_str  = row.get('Area', '0').replace('m²', '').replace(',', '').strip()
                roi_str   = row.get('ROI', '0').replace('%', '').strip()
                payback_str = row.get('Payback', '0').strip()
                status    = row.get('Status', '').strip().lower()

                if status not in ['available', 'free', 'ხელმისაწვდომი', '']:
                    continue

                price = float(price_str) if price_str else 0
                area  = float(area_str)  if area_str  else 0
                roi   = float(roi_str)   if roi_str   else 0
                payback = float(payback_str) if payback_str else 0

                if price > 0:
                    plots.append({
                        'id':      row.get('ID', '').strip(),
                        'zone':    row.get('Zone', '').strip(),
                        'style':   row.get('Style', '').strip(),
                        'price':   price,
                        'area':    area,
                        'roi':     roi,
                        'payback': payback,
                    })
            except (ValueError, KeyError):
                continue
        return plots
    except Exception as e:
        print(f"Inventory fetch error: {e}")
        return []

def get_plots():
    global cached_plots, last_fetch_time
    now = time.time()
    with cache_lock:
        if now - last_fetch_time > FETCH_INTERVAL or not cached_plots:
            plots = fetch_and_parse_inventory()
            if plots:
                cached_plots = plots
                last_fetch_time = now
                print(f"Successfully cached {len(cached_plots)} plots from Google Sheets.")
        return cached_plots

def search_inventory(plots, query):
    q = query.lower()
    zone_map = {'la': 'LA', 'lb': 'LB', 'lc': 'LC', 'ld': 'LD',
                'კანიონ': 'LA', 'პირველ': 'LB', 'მეორ': 'LC', 'მესამ': 'LD', 'apart': 'APART'}
    zones = [v for k, v in zone_map.items() if k in q]

    max_p, min_p = None, None
    prices = re.findall(r'\$?([\d,]+)', query)
    if prices:
        nums = [float(p.replace(',', '')) for p in prices]
        if len(nums) >= 2:
            min_p, max_p = min(nums), max(nums)
        elif nums[0] < 5000:
            max_p = nums[0] * 1000
        else:
            max_p = nums[0]

    results = [p for p in plots if
               (not zones or p['zone'] in zones) and
               (not max_p or p['price'] <= max_p) and
               (not min_p or p['price'] >= min_p)]
    results.sort(key=lambda x: x['price'])
    return results[:5], zones, max_p, min_p

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

ინვესტიცია (Turnkey): ROI 9-12%/წ | 60% შემოსავალი მფლობელს, 40% კომპანიას (კომპანია ფარავს ყველა ხარჯს) | 14 დღე/წ უფასო სარგებლობა | ზუსტი გათვლები — PDF/Excel-ით.

მშენებლობა: სკანდინავიური სენდვიჩ-პანელი | Turnkey (ავეჯი+ტექნიკა) ან შავი/თეთრი კარკასი | მზის პანელები ფასშია.

ინფრასტრუქტურა: რესტორანი, სპა, სპორტი, საბავშვო მოედანი, დაცვა 24/7.

იურიდიული: საჯარო რეესტრი. უცხოელებს შეუძლიათ შეძენა (არასასოფლო-სამეურნეო სტატუსი). 10-წლიანი გაქირავების ხელშეკრულება.

=== წესები ===
არ გამოთვალო კვ.მ ფასი ან კონკრეტული მოგება ჩატში.
არ გამოიგონო სახელები, გადახდის გრაფიკი ან განვადების ზუსტი პირობები.
უცნობ კითხვაზე: "ამ დეტალებზე ჩვენი სპეციალისტი პირადად გაგესაუბრებათ — გთხოვთ, დაგვიტოვოთ ნომერი."
"""

# user_id -> Gemini ChatSession  (Groq fallback: list of messages)
user_gemini_sessions = {}
user_groq_history    = {}
sessions_lock        = threading.Lock()

def call_gemini(user_id, user_message, context_msg=""):
    """Gemini-ზე გამოძახება — სესია შენახულია მომხმარებლის მიხედვით."""
    global user_gemini_sessions
    with sessions_lock:
        if user_id not in user_gemini_sessions:
            session = gemini_model.start_chat(history=[])
            # სისტემის პრომპტს ვუგზავნით პირველ შეტყობინებად
            session.send_message(f"[სისტემის ინსტრუქცია]\n{SYSTEM_PROMPT}\n[ინსტრუქცია დასრულდა]")
            user_gemini_sessions[user_id] = session
        session = user_gemini_sessions[user_id]

    full_message = user_message
    if context_msg:
        full_message = f"{user_message}\n\n[ინვენტარიდან]:\n{context_msg}"

    response = session.send_message(full_message)
    return response.text

def call_groq_fallback(user_id, user_message, context_msg=""):
    """Groq fallback — Gemini ვერ მუშაობს ან rate-limit-ზეა."""
    if not groq_client:
        return None
    with sessions_lock:
        if user_id not in user_groq_history:
            user_groq_history[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
        history = user_groq_history[user_id]

    history.append({"role": "user", "content": user_message})
    if context_msg:
        history.append({"role": "system", "content": f"ინვენტარი: {context_msg}"})

    # ისტორია შეკვეცილი
    sys_msgs    = [m for m in history if m['role'] == 'system']
    other_msgs  = [m for m in history if m['role'] != 'system']
    trimmed     = sys_msgs[:1] + other_msgs[-6:]

    for model_name in ["llama-3.3-70b-versatile", "gemma2-9b-it"]:
        try:
            comp = groq_client.chat.completions.create(
                model=model_name, messages=trimmed,
                temperature=0.5, max_tokens=900)
            text = comp.choices[0].message.content
            history.append({"role": "assistant", "content": text})
            if len(history) > 10:
                user_groq_history[user_id] = history[:1] + history[-6:]
            return text
        except Exception as e:
            print(f"Groq {model_name} error: {e}")
    return None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    uid = message.chat.id
    with sessions_lock:
        user_gemini_sessions.pop(uid, None)
        user_groq_history.pop(uid, None)
    bot.reply_to(message,
        "გამარჯობა! მე ვარ Green Canyon Eco Village-ის AI კონსულტანტი 🏔️\n\n"
        "სიამოვნებით გიპასუხებთ პროექტის შესახებ — ფასები, ზონები, ROI, გადახდის პირობები და სხვა.\n\n"
        "რით შეიძლება დაგეხმაროთ?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    uid        = message.chat.id
    query_text = message.text

    # ── ინვენტარის კონტექსტი ──────────────────────────────────────────────
    context_msg = ""
    plots = get_plots()
    if plots:
        keywords = ['ვარიანტ','ნაკვეთ','კოტეჯ','თავისუფალ','ყველაზე','რომელი',
                    'საუკეთეს','ფასი','ღირს','რა გაქვთ','roi','უკუგება','ზონა','la','lb','lc','ld']
        matching_plots, zones, max_p, min_p = search_inventory(plots, query_text)
        if zones or max_p or min_p or any(w in query_text.lower() for w in keywords):
            if matching_plots:
                context_msg = f"ხელმისაწვდომი {len(matching_plots)} ვარიანტი:\n"
                for r in matching_plots[:4]:
                    context_msg += (f"• კოდი {r['id']} | {r['zone']} ზონა | {r['style']} | "
                                    f"${r['price']:.0f} | {r['area']:.0f}მ² | ROI {r['roi']}%\n")
            else:
                context_msg = "მითითებული ფილტრებით ხელმისაწვდომი ვარიანტი ვერ მოიძებნა."

    # ── AI გამოძახება: Gemini → Groq fallback ─────────────────────────────
    response_text = None

    if gemini_model:
        try:
            print(f"[Gemini] user={uid} query='{query_text[:50]}'")
            response_text = call_gemini(uid, query_text, context_msg)
            print(f"[Gemini] OK, {len(response_text)} chars")
        except Exception as e:
            print(f"[Gemini] FAILED: {e} — switching to Groq fallback")
            response_text = None

    if response_text is None:
        print(f"[Groq fallback] user={uid}")
        response_text = call_groq_fallback(uid, query_text, context_msg)

    if response_text is None:
        bot.reply_to(message, "⚠️ სამწუხაროდ, ამ მომენტში სერვისი გადატვირთულია. გთხოვთ, 1-2 წუთში სცადოთ ხელახლა.")
        return

    # ── ლოგირება + პასუხი ─────────────────────────────────────────────────
    fallback_phrases = ["სპეციალისტი გაგესაუბრებათ", "ჩვენი სპეციალისტი", "დაგვიტოვოთ ნომერი"]
    if any(phrase in response_text for phrase in fallback_phrases):
        log_unanswered_question(uid, query_text, response_text)

    bot.reply_to(message, response_text)

# ── Polling Loop ──────────────────────────────────────────────────────────
import sys
time.sleep(1)
print("Starting polling loop (threaded)...")
offset = None
consecutive_conflicts = 0
while True:
    try:
        updates = bot.get_updates(offset=offset, timeout=30)
        consecutive_conflicts = 0
        if updates:
            for update in updates:
                offset = update.update_id + 1
            bot.process_new_updates(updates)
    except Exception as e:
        err_msg = str(e).lower()
        if "conflict" in err_msg or "409" in err_msg:
            consecutive_conflicts += 1
            if consecutive_conflicts >= 3:
                print("Conflict 409 x3 — exiting.")
                sys.exit(1)
            print(f"Conflict 409 ({consecutive_conflicts}/3). Sleeping 15s...")
            time.sleep(15)
        else:
            print(f"Polling error: {e}. Retry in 5s...")
            time.sleep(5)
