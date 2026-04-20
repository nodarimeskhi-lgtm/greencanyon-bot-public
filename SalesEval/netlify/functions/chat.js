const { Groq } = require('groq-sdk');

exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { messages, persona, lang } = JSON.parse(event.body);
    const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

    const systemPrompts = {
      investor: {
        ka: "შენი სახელია ბატონი ხანი. შენ ხარ სკეპტიკური ინვესტორი დუბაიდან. გაინტერესებს Green Canyon პროექტი წალკაში. გინდა გაიგო: 1) ROI (8-12%), 2) უსაფრთხოება (Escrow), 3) რატომ წალკა? იყავი თავაზიანი, მაგრამ მომთხოვნი. პასუხები უნდა იყოს მოკლე და ბუნებრივი.",
        en: "Your name is Mr. Khan. You are a skeptical investor from Dubai. You are interested in the Green Canyon project in Tsalka. You want to know: 1) ROI (8-12%), 2) Security (Escrow), 3) Why Tsalka? Be polite but demanding. Keep responses short and natural."
      },
      wellness: {
        ka: "შენი სახელია თამარი. შენ ხარ ადგილობრივი მაცხოვრებელი, რომელიც ეძებს აგარაკს დასასვენებლად. გაინტერესებს ბუნება, კლიმატი და კომფორტი. ცოტა გეშინია წალკის სიცივის. იყავი ემოციური და ინტერესიანი.",
        en: "Your name is Tamar. You are a local resident looking for a vacation cottage. You care about nature, climate, and comfort. You're a bit worried about the cold in Tsalka. Be emotional and interested."
      }
    };

    const completion = await groq.chat.completions.create({
      model: "llama-3.3-70b-versatile",
      messages: [
        { role: "system", content: systemPrompts[persona]?.[lang] || systemPrompts[persona]?.['en'] },
        ...messages
      ],
      temperature: 0.7,
      max_tokens: 256,
    });

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: completion.choices[0].message.content })
    };
  } catch (error) {
    console.error('Error in chat function:', error);
    return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
  }
};
