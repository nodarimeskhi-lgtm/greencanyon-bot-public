const { Groq } = require('groq-sdk');

exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const { history, lang } = JSON.parse(event.body);
    const groq = new Groq({ apiKey: process.env.GROQ_API_KEY });

    const evalPrompt = `
      შენ ხარ გაყიდვების ექსპერტი. შეაფასე შემდეგი დიალოგი Green Canyon პროექტის გაყიდვების აგენტსა და პოტენციურ კლიენტს შორის.
      
      კრიტერიუმები:
      1. ინფორმაციის სიზუსტე (Accuracy): ROI 8-12%, ფასი $59,500-დან, 36 თვიანი განვადება, Escrow გარანტია.
      2. საუბრის მანერა (Manner): თავდაჯერებულობა, ტონი, ემპათია.
      3. Soft Skills: აქტიური მოსმენა, წინააღმდეგობების დაძლევა.

      დააბრუნე პასუხი JSON ფორმატში:
      {
        "accuracy": (0-100),
        "manner": (0-100),
        "soft": (0-100),
        "total": (0-10),
        "feedback": ["რჩევა 1", "რჩევა 2", ...] (ქართულად ან ინგლისურად შესაბამისად)
      }

      დიალოგი:
      ${JSON.stringify(history)}
    `;

    const completion = await groq.chat.completions.create({
      model: "llama-3.3-70b-versatile",
      messages: [{ role: "system", content: "You are a professional sales trainer. Return only JSON." }, { role: "user", content: evalPrompt }],
      temperature: 0.1,
      response_format: { type: "json_object" }
    });

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: completion.choices[0].message.content
    };
  } catch (error) {
    console.error('Error in evaluate function:', error);
    return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
  }
};
