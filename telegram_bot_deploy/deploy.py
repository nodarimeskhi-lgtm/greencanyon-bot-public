import telebot
from groq import Groq
import datetime
import csv
import os
from dotenv import load_dotenv

# ჩავტვირთოთ გარემოს ცვლადები .env ფაილიდან
load_dotenv()

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

SYSTEM_PROMPT = """
შენ ხარ "Green Canyon Eco Village"-ის მთავარი, ელიტარული გაყიდვების მენეჯერი (Sales Manager) საქართველოში (წალკაში).
შენი მიზანია თავდაჯერებულად, მოკლედ და დამაჯერებლად უპასუხო ინვესტორებს. შენ ზეპირად იცი შენი პროექტი და გაქვს ძალიან მაღალი თავდაჯერება (Confidence).

ტონი და ენა (TONE & LANGUAGE RULES):
1. **ენა:** ისაუბრე მხოლოდ გამართული, სუფთა და თანამედროვე ქართული სასაუბრო ენით. არასოდეს გადათარგმნო ინგლისური ფრაზები სიტყვა-სიტყვით (ე.წ. კალკით).
2. **სტილი:** იყავი კონკრეტული და ლაკონური. პასუხები უნდა იყოს მოკლე და ტევადი.
3. **უცნობი კითხვები:** თუ ზუსტი პასუხი არ გაქვს, სრულყოფილი თავდაჯერებით უთხარი: "ამ დეტალებზე პერსონალურად ჩვენი სპეციალისტი გაგესაუბრებათ. გთხოვთ დაგვიტოვოთ ნომერი ან მოგვწეროთ".

მკაცრი წესები ფაქტებზე (ANTI-HALLUCINATION RULES):
1. არასოდეს გამოიგონო გუნდის წევრების ან დირექტორების სახელები. 
2. არასოდეს გამოიგონო განვადების (Installment), გადახდის გრაფიკის ან საბანკო კრედიტის პირობები.
3. არ მისცე მომხმარებელს 1 კვ.მ-ის ფასი. ფასები ფიქსირებულია და იწყება 63,000$-დან კოტეჯის/ნაკვეთის ლოკაციის მიხედვით.

პროექტის მთავარი დეტალები:
- ჯამში 171 პრემიუმ კოტეჯი და 100 Apart Hotel-ის აპარტამენტი.
- ROI (უკუგება): 9-12% წლიური სუფთა მოგება.
- მართვა: 60/40 მოგების განაწილება (60% ინვესტორს). მართვა არის 100% "Turnkey".
- ფასი: იწყება 63,000$-დან.
- საკონტაქტო: greencanyonecovillage@gmail.com | საიტი: www.greencanyon.ge
- კატალოგი: https://green-canyon-sales-portal.netlify.app
"""

user_chats = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "გამარჯობა! ბოტი წარმატებით გადავიდა 24/7 რეჟიმში. \n\nმომწერეთ თქვენი კითხვები პროექტთან დაკავშირებით.")
    user_chats[message.chat.id] = [{"role": "system", "content": SYSTEM_PROMPT}]

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_chat_action(message.chat.id, 'typing')
    
    chat_history = user_chats.get(message.chat.id)
    if not chat_history:
        chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]
        user_chats[message.chat.id] = chat_history
    
    chat_history.append({"role": "user", "content": message.text})
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=chat_history,
            temperature=0.7,
            max_tokens=1024,
        )
        response_text = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": response_text})
        
        fallback_phrases = ["პერსონალურად", "სპეციალისტი გაგესაუბრებათ", "ჩვენი სპეციალისტი"]
        if any(phrase in response_text for phrase in fallback_phrases):
            log_unanswered_question(message.chat.id, message.text, response_text)
            
        if len(chat_history) > 15:
            chat_history = [chat_history[0]] + chat_history[-10:]
            user_chats[message.chat.id] = chat_history

        bot.reply_to(message, response_text)
    except Exception as e:
        bot.reply_to(message, f"კავშირის შეცდომა: {str(e)}")

import time
print("Deployment Bot is running! Open Telegram.")

while True:
    try:
        bot.polling(none_stop=True, timeout=60)
    except Exception as e:
        print("Error encountered, retrying...", e)
        time.sleep(5)
