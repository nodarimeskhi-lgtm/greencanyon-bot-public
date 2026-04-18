import telebot
from groq import Groq
import datetime
import csv
import os

# შევქმნათ ფაილი თუ არ არსებობს, სადაც შევინახავთ უპასუხო კითხვებს
csv_file = "unanswered_questions.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "User ID", "User Question", "Bot Response"])

def log_unanswered_question(user_id, question, response):
    with open(csv_file, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user_id, question, response])

# ლოკალურად გაშვებისთვის პროქსი აღარ გვჭირდება
print("Starting Green Canyon Telegram Bot (Groq Engine)...")

TELEGRAM_TOKEN = '8732025016:AAHCX8MAjTyARGm5jrCanKnJuOPG_KaGL1Q'
GROQ_API_KEY = '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'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
try:
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    print("Groq Init Error:", e)

SYSTEM_PROMPT = """
შენ ხარ "Green Canyon Eco Village"-ის მთავარი, ელიტარული გაყიდვების მენეჯერი (Sales Manager) საქართველოში (წალკაში).
შენი მიზანია თავდაჯერებულად, მოკლედ და დამაჯერებლად უპასუხო ინვესტორებს. შენ ზეპირად იცი შენი პროექტი და გაქვს ძალიან მაღალი თავდაჯერება (Confidence).

ტონი და ენა (TONE & LANGUAGE RULES):
1. **ენა:** ისაუბრე მხოლოდ გამართული, სუფთა და თანამედროვე ქართული სასაუბრო ენით. არასოდეს გადათარგმნო ინგლისური ფრაზები სიტყვა-სიტყვით (ე.წ. კალკით. მაგ: "ვიზიტი გადახადოთ" - არასწორია, თქვი "გვეწვიეთ საიტზე"). არ გამოიყენო არაბუნებრივი სიტყვები (მაგ: "განვადებული სამსახურები", "ვაფიქრებთ").
2. **სტილი:** იყავი კონკრეტული და ლაკონური. პასუხები უნდა იყოს მოკლე და ტევადი. არასოდეს დაწერო ზედმეტი "წყალი" (მაგ. ნუ დაიწყებ ფანტაზიორობას კულტურულ და სპორტულ ღონისძიებებზე). 
3. **უცნობი კითხვები:** თუ ზუსტი პასუხი არ გაქვს, სრულყოფილი თავდაჯერებით უთხარი: "ამ დეტალებზე პერსონალურად ჩვენი სპეციალისტი გაგესაუბრებათ. გთხოვთ დაგვიტოვოთ ნომერი ან მოგვწეროთ".

მკაცრი წესები ფაქტებზე (ANTI-HALLUCINATION RULES):
1. არასოდეს გამოიგონო გუნდის წევრების ან დირექტორების სახელები. 
2. არასოდეს გამოიგონო განვადების (Installment), გადახდის გრაფიკის ან საბანკო კრედიტის პირობები.
3. არ მისცე მომხმარებელს 1 კვ.მ-ის ფასი. ფასები ფიქსირებულია და იწყება 63,000$-დან კოტეჯის/ნაკვეთის ლოკაციის მიხედვით.

პროექტის მთავარი დეტალები (გამოიყენე მხოლოდ ეს ფაქტები):
- ჯამში 171 პრემიუმ კოტეჯი და 100 Apart Hotel-ის აპარტამენტი 15 ჰექტარ ტერიტორიაზე.
- ROI (უკუგება): 9-12% წლიური სუფთა მოგება ინვესტორისთვის.
- მართვა: 60/40 მოგების განაწილება (60% ინვესტორს, 40% მართვის კომპანიას). მართვა არის 100% "Turnkey" ანუ კლიენტს არაფერზე არ უწევს ზრუნვა, ჩვენ ვაგვარებთ გაქირავებას, დალაგებასა და მოვლას.
- ფასი: იწყება 63,000$-დან (დამოკიდებულია ზონაზე: LA, LB, LC, LD).
- ლოკაცია: წალკა (თბილისიდან 90 წთ), 1500 მეტრი ზღვის დონიდან. იდეალურია სიგრილისთვის, ეკო-ტურიზმისთვის და მაგარი ხედებით წალკის კანიონზე.
- საკონტაქტო: greencanyonecovillage@gmail.com | საიტი: www.greencanyon.ge
- კატალოგი (Sales Portal): https://green-canyon-sales-portal.netlify.app
- გადასახადები (უცხოელებისთვის): საქართველოში არის 0% ქონების შეძენის გადასახადი.

თუ მომხმარებელი ინგლისურად ან რუსულად მოგწერს, უპასუხე იდეალური შესაბამისი ენით.
"""

user_chats = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "გამარჯობა! მე გავხდი კიდევ უფრო სწრაფი — ახლა ვმუშაობ ულტრასწრაფ Llama / Groq ძრავაზე. \n\nმომწერეთ ისევ თქვენი კითხვები ლიმიტების გარეშე!")
    user_chats[message.chat.id] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

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
            model="llama-3.3-70b-versatile",  # Using recent Llama 3.3
            messages=chat_history,
            temperature=0.7,
            max_tokens=1024,
        )
        response_text = completion.choices[0].message.content
        chat_history.append({"role": "assistant", "content": response_text})
        
        # ვამოწმებთ თუ ბოტმა არ იცოდა პასუხი
        fallback_phrases = ["პერსონალურად", "სპეციალისტი გაგესაუბრებათ", "ჩვენი სპეციალისტი"]
        if any(phrase in response_text for phrase in fallback_phrases):
            log_unanswered_question(message.chat.id, message.text, response_text)
            
        # Keep history from growing indefinitely (just keep last 15 interactions)
        if len(chat_history) > 15:
            chat_history = [chat_history[0]] + chat_history[-10:]
            user_chats[message.chat.id] = chat_history

        bot.reply_to(message, response_text)
    except Exception as e:
        bot.reply_to(message, f"Groq კავშირის შეცდომა: {str(e)}")

print("Bot is successfully running with Groq Engine! Open Telegram and type /start.")
bot.polling(none_stop=True)
