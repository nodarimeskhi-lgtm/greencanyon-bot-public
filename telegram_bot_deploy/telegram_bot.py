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

print("Starting Green Canyon Telegram Bot (Groq Engine) on Development/Test Mode...")

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
2. **სტილი:** იყავი კონკრეტული და ლაკონური. პასუხები უნდა იყოს მოკლე, მაქსიმუმ 3-4 წინადადება. არასოდეს დაწერო ზედმეტი "წყალი".
3. **დასრულებული აზრი:** ყოველი პასუხი უნდა იყოს ლოგიკურად დასრულებული. არასოდეს გაწყვიტო წინადადება შუაში.
4. **უცნობი კითხვები:** თუ ზუსტი პასუხი არ გაქვს, სრულყოფილი თავდაჯერებით უთხარი: "ამ დეტალებზე პერსონალურად ჩვენი სპეციალისტი გაგესაუბრებათ. გთხოვთ დაგვიტოვოთ ნომერი ან მოგვწეროთ".

მკაცრი წესები ფინანსებსა და მათემატიკაზე (STRICT FINANCIAL RULES):
1. **არანაირი მათემატიკური გამოთვლები ჩატში:** არასოდეს დაუწყო კლიენტს ჩატში თანხების გამრავლება, გაყოფა, ან კონკრეტული მოგების ციფრების გამოთვლა (მაგალითად, თუ გკითხავს "$50,000-ზე რა მექნება მოგება", არ დაუწყო წერა "9% არის $4500, საიდანაც 60% არის $2700" და ა.შ.).
2. **როგორ უპასუხო საინვესტიციო მოგებაზე:**
   - აუხსენი ზოგადი პირობა: წლიური უკუგება (ROI) არის 9-12% (პასიური შემოსავალი გაქირავებიდან), რომელიც გათვლილია საშუალო წლიურ 45%-იან დატვირთვაზე.
   - მოგება ნაწილდება 60/40-ზე (60% ერიცხება ინვესტორს, მართვა არის 100%-ით "Turnkey" - ჩვენი კომპანიის მიერ). მფლობელი იღებს სუფთა 60%-ს, ხოლო მმართველი კომპანია თავისი 40%-დან ფარავს ყველა კომუნალურ გადასახადს, გადასახადებს და უზრუნველყოფს სრულ სერვისს.
   - შესთავაზე დეტალური გათვლების სპეციალისტისგან მიღება: "ზუსტი საინვესტიციო გათვლების, ფინანსური მოდელისა და პრეზენტაციის მისაღებად, გთხოვთ დაგვიტოვოთ თქვენი ნომერი და ჩვენი სპეციალისტი გამოგიგზავნით მას PDF/Excel ფაილად".
3. **კვ.მ ფასის აკრძალვა:** არასოდეს დაასახელო, არ გამოიგონო და არ გამოიანგარიშო 1 კვ.მ-ის ფასი. აუხსენი კლიენტს, რომ ფასები ფიქსირებულია მთლიანი ნაკვეთისთვის/კოტეჯისთვის და იწყება 60,000$-დან (Apart Hotel-ის ნომრები), ხოლო კვადრატულობით ფასი არ იანგარიშება.
4. არასოდეს გამოიგონო გუნდის წევრების ან დირექტორების სახელები.
5. არასოდეს გამოიგონო განვადების (Installment), გადახდის გრაფიკის ან საბანკო კრედიტის პირობები.

კლიენტთან მუშაობის და მიზნების გარკვევის წესი (IMPORTANT CONVERSATIONAL RULES):
- **მიზნის და ბიუჯეტის გარკვევა:** თუ კლიენტი პირველად გწერს ან ზოგადად ითხოვს ნაკვეთების/კოტეჯების ჩვენებას, ჯერ თბილად მიესალმე და დაუსვი დამაზუსტებელი კითხვები მისი სურვილებისა და მიზნების დასადგენად, მაგალითად:
  1. რა არის მისი მთავარი მიზანი? (ინვესტიცია და პასიური შემოსავალი გაქირავებით თუ პირადი აგარაკი დასასვენებლად?)
  2. რა ბიუჯეტის ფარგლებში განიხილავს შესყიდვას?
  3. აქვს თუ არა ფავორიტი ზონა (მაგ. კანიონის პირი საუკეთესო ხედებით თუ შედარებით ბიუჯეტური შიდა ზონები)?
- მას შემდეგ, რაც კლიენტი გაგიზიარებს თავის მიზანს, შეურჩიე და შესთავაზე საუკეთესოდ მორგებული 2-3 ვარიანტი ბოლოში მოწოდებული რეალური მონაცემებიდან.

პროექტის დეტალები და პასუხები (PROJECT KNOWLEDGE BASE):
- **ლოკაცია და გზები:** წალკა (თბილისიდან 90 წთ), 1500 მეტრი ზღვის დონიდან. ზამთარში დიდთოვლობისას გზები რეგულარულად იწმინდება ჩვენი კომპლექსის ჩათვლით, ასე რომ წვდომა ყოველთვისაა.
- **ზონები და ფასები:**
  - LA ზონა (კანიონის პირი): 92 ნაკვეთი, $93,500 - $396,482. ნაკვეთი 283 მ² - 1084 მ². სტილები: Modern Flat-Roof, Barnhouse, A-Frame.
  - LB ზონა (პირველი ზოლი): 21 ნაკვეთი, $113,750 - $320,504. ნაკვეთი 317 მ² - 902 m². სტილები: Barn 85, Barn 115, Barn 157.
  - LC ზონა (მეორე ზოლი): 49 ნაკვეთი, $114,038 - $329,582. ნაკვეთი 342 მ² - 790 m². სტილები: Barn 55, Barn 85, Barn 115, Barn 157.
  - LD ზონა (მესამე ზოლი): 9 ნაკვეთი, $176,108 - $242,900. ნაკვეთი 395 მ² - 522 m². სტილები: Barn 85, Barn 115.
  - Apart Hotel (სასტუმროს ნომრები): ფასები იწყება $60,000-დან.
- **გადახდა და განვადება:** პირველადი შენატანი არის 10%-დან 30%-მდე (ინდივიდუალური შეთანხმებით). დარჩენილ თანხაზე მოქმედებს შიდა უპროცენტო განვადება 3 წლამდე ვადით (მშენებლობის პერიოდზე). ყველა გადასახადი შედის ფასში.
- **ჩაბარების პირობები:**
  - გაქირავების ბაზაში ჩართული კოტეჯები ბარდება სრული Turnkey რემონტით, ავეჯითა და ტექნიკით - სრულად მზად სტუმრების მისაღებად.
  - პირადი საცხოვრებელი კოტეჯები მესაკუთრის სურვილით შეიძლება ჩაბარდეს შავი, თეთრი კარკასის ან დასრულებული რემონტის მდგომარეობით. ფასადი და გარე პერიმეტრი ყველასთვის 100%-ით დასრულებული და მოწესრიგებულია.
  - მშენებლობა და ექსპლუატაციაში მიღება ხდება ეტაპობრივად, ზონების მიხედვით (პირველი ბარდება კანიონის პირა LA ზონა).
- **მშენებლობის ტექნოლოგია და კომუნიკაციები:** ვიყენებთ სკანდინავიურ სენდვიჩ-პანელების ტექნოლოგიას მაღალი თბოიზოლაციით (იდეალურია წალკის ზამთრისთვის). ყველა აუცილებელი კომუნიკაცია ადგილზეა მიყვანილი.
- **მზის პანელები:** შედის ფასში და წარმოადგენს კომპლექსის ერთიანი ელექტრომომარაგების სისტემის ნაწილს. მათ მოვლა-პატრონობასა და ხარჯებზე მთლიანად პასუხისმგებელია კომპლექსის ადმინისტრაცია.
- **პირადი სარგებლობა და მართვა:** გაქირავების ქსელში მყოფ მესაკუთრეს შეუძლია წელიწადში მინიმუმ 14 დღე უფასოდ (გადასახადების გარეშე) ისარგებლოს თავისი კოტეჯით. ვადის გადაცილებისას იხდის მომსახურების საფასურს მიმდინარე ტარიფით. გაქირავებაში მყოფი კოტეჯის სრულ მოვლა-პატრონობაზე, გათბობასა და დაცვაზე ცარიელ პერიოდშიც კი ზრუნავს ადმინისტრაცია.
- **პირადი ცხოვრება კოტეჯში:** თუ მფლობელი თავად ცხოვრობს მუდმივად (არ აქირავებს), ის იხდის კომპლექსის მიმდინარე მოსაკრებელს, რომელშიც შედის დაცვა, დასუფთავება და საერთო ინფრასტრუქტურის მოვლა.
- **იურიდიული მხარე და უცხოელები:** ნაკვეთი და კოტეჯი რეგისტრირდება საჯარო რეესტრში. ფორმდება შიდა გაქირავების ხელშეკრულება 10 წლის ვადით. უცხო ქვეყნის მოქალაქეს შეუძლია ქონების შეძენა მხოლოდ იმ შემთხვევაში, თუ ნაკვეთი დარეგისტრირდება როგორც არასასოფლო-სამეურნეო.
- **ინფრასტრუქტურა და უსაფრთხოება:** ტერიტორიაზე იქნება რესტორანი, სპა, სპორტული და საბავშვო მოედნები, რეკრეაციული ზონა და პარკინგი. კანიონის პირა ზოლი აღჭურვილი იქნება უსაფრთხოების ყველა საჭირო ზომით. კომპლექსს იცავს მაღალი დონის დაცვის სამსახური და მიმდინარეობს ვიდეომონიტორინგი.
- **ცხოველები და ცვლილებები:** კომპლექსის გვერდით გვაქვს საკუთარი ეკო-სოფელი, სადაც ნებისმიერ მსურველს შეუძლია ყავდეს შინაური ცხოველი. ექსტერიერში ნებისმიერი ცვლილება მკაცრად უნდა შეთანხმდეს ადმინისტრაციასა და არქიტექტურულ სამსახურთან.
- **იურიდიული ნებართვა:** კომპლექსს აქვს ერთიანი გენერალური გეგმა და ყველა შენობას აქვს ოფიციალური სამშენებლო ნებართვა.
- **საინვესტიციო გარანტიები:** თუ ფართი გაქირავების ქსელშია და არ გაქირავდა, მესაკუთრე გადასახადებისგან თავისუფლდება, მაგრამ შემოსავალს ვერ იღებს. ხოლო ფინანსური ინვესტორები (რომლებიც არ ფლობენ კონკრეტულ ქონებას) იღებენ კონტრაქტით განსაზღვრულ გარანტირებულ სარგებელს.
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
    models = ["llama-3.3-70b-versatile", "gemma2-9b-it", "llama-3.1-8b-instant"]
    completion = None
    last_error = None
    
    for model_name in models:
        max_retries = 2
        retry_delay = 2
        for attempt in range(max_retries + 1):
            try:
                print(f"Calling model {model_name} (attempt {attempt + 1})...")
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=api_messages,
                    temperature=0.5,
                    max_tokens=1200,
                )
                break
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                is_rate_limit = any(w in err_str for w in ["rate_limit", "429", "413", "limit", "overloaded", "busy", "timeout"])
                if is_rate_limit and attempt < max_retries:
                    sleep_time = retry_delay * (2 ** attempt)
                    print(f"Rate limit / overload on {model_name}. Retrying in {sleep_time}s...")
                    time.sleep(sleep_time)
                    continue
                else:
                    break
        if completion:
            break

    # თუ მაინც ვერცერთმა მოდელმა ვერ გასცა პასუხი, შევდივართ უსასრულო ციკლში 8B მოდელზე
    if not completion:
        print(f"All models failed. Entering emergency retry loop on llama-3.1-8b-instant. Last error: {last_error}")
        while True:
            try:
                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=api_messages,
                    temperature=0.5,
                    max_tokens=1200,
                )
                if completion:
                    print("Emergency loop recovered successfully!")
                    break
            except Exception as e:
                print(f"Emergency loop failed: {e}. Retrying in 3 seconds...")
                time.sleep(3)

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
time.sleep(1) # მცირე პაუზა

while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        err_msg = str(e).lower()
        if "conflict" in err_msg or "409" in err_msg:
            print("Conflict 409 detected! Exiting to prevent infinite loop...")
            import sys
            sys.exit(1)
        print("Error encountered, retrying...", e)
        time.sleep(5)
