const https = require('https');

exports.handler = async (event, context) => {
  const apiKey = process.env.GROQ_API_KEY;

  if (!apiKey) {
    return { statusCode: 500, body: JSON.stringify({ error: "API key missing", version: "v5.1-Stable" }) };
  }

  try {
    const { messages, persona, lang } = JSON.parse(event.body);

    const projectKnowledge = `
      STRICT FACTS (DO NOT DEVIATE):
      - Project: Green Canyon, modern Eco-settlement.
      - Location: Tsalka, Georgia.
      - ROI: 8-12% annually.
      - Safety: Secure Escrow-based accounts, Bank guarantees.
      - Amenities: Energy-efficient modern cabins, panoramic Tsalka views.
      - RULES: Never repeat user questions. Logical, short answers only.
    `;

    const systemPrompts = {
      investor: {
        ka: `შენ ხარ ბატონი ხანი, სკეპტიკოსი ინვესტორი. 
        მთავარი წესი: არასოდეს გაიმეორო ან შეაჯამო აგენტის ნათქვამი. პირდაპირ გადადი შენს კითხვაზე.
        საუბრის სტილი: იყავი ძალიან მოკლე, კონკრეტული და ეჭვიანი. 
        მიზანი: დაუსვი მომდევნო რთული კითხვა ROI-ზე ან უსაფრთხოებაზე.`,
        en: `Your name is Mr. Khan, a skeptical investor. 
        MAIN RULE: NEVER repeat or summarize what the agent said. Go directly to your question. 
        Style: Be very short, direct, and suspicious. 
        Goal: Ask your next tough question about ROI or safety immediately.`
      },
      wellness: {
        ka: `შენ ხარ თამარი, ოჯახისთვის სახლის მაძიებელი. 
        მთავარი წესი: არასოდეს გაიმეორო აგენტის ნათქვამი "დამტკიცების" მიზნით. პირდაპირ გამოხატე შენი ემოცია ან კითხვა.
        საუბრის სტილი: იყავი მოკლე და ბუნებრივი. 
        მიზანი: პირდაპირ კითხე მომდევნო დეტალი (სითბო, ბავშვები, ბუნება).`,
        en: `Your name is Tamar, looking for a family home. 
        MAIN RULE: NEVER repeat what the agent said. Go directly to your emotion or question. 
        Style: Be short and natural. 
        Goal: Ask your next question (warmth, kids, nature) immediately.`
      }
    };

    let groqMessages = (messages || []).slice(-10); 
    let introContext = "";
    
    if (groqMessages.length > 0 && groqMessages[0].role === 'assistant') {
        const firstMsg = groqMessages.shift();
        introContext = `\n\nIntro: "${firstMsg.content}"`;
    }

    const models = ["llama-3.3-70b-versatile", "gemma2-9b-it", "llama-3.1-8b-instant"];
    let finalCompletion = null;
    let lastError = null;
    const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

    for (const modelName of models) {
      let success = false;
      const maxRetries = 2;
      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
          const postData = JSON.stringify({
            model: modelName,
            messages: [
              { role: "system", content: (systemPrompts[persona]?.[lang] || systemPrompts[persona]?.['en'] || "You are a lead.") + "\nInstruction: DO NOT summarize or repeat the agent's points. Remember previous answers and do not ask redundant questions. Be direct and concise." + introContext },
              ...groqMessages
            ],
            temperature: 0.5, 
            max_tokens: 1024,
          });

          const response = await new Promise((resolve, reject) => {
            const options = {
              hostname: 'api.groq.com',
              path: '/openai/v1/chat/completions',
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
                'Content-Length': Buffer.byteLength(postData)
              }
            };

            const req = https.request(options, (res) => {
              res.setEncoding('utf8');
              let body = '';
              res.on('data', (chunk) => body += chunk);
              res.on('end', () => resolve({ status: res.statusCode, data: body }));
            });

            req.on('error', (e) => reject(e));
            req.write(postData);
            req.end();
          });

          const groqData = JSON.parse(response.data);

          if (response.status === 200) {
            finalCompletion = groqData;
            success = true;
            break;
          } else {
            const errMsg = groqData.error?.message || "Connection issue.";
            throw new Error(`HTTP ${response.status}: ${errMsg}`);
          }
        } catch (e) {
          lastError = e;
          const errStr = e.message.toLowerCase();
          const isRateLimit = errStr.includes("rate_limit") || errStr.includes("429") || errStr.includes("413") || errStr.includes("limit") || errStr.includes("overloaded") || errStr.includes("busy") || errStr.includes("timeout");
          if (isRateLimit && attempt < maxRetries) {
            await delay(2000 * Math.pow(2, attempt));
          } else {
            break;
          }
        }
      }
      if (success) {
        break;
      }
    }

    if (!finalCompletion) {
      // Emergency retry loop on 8B model to guarantee an answer, trying every 3 seconds
      console.log(`All models failed. Entering emergency retry loop on llama-3.1-8b-instant. Last error: ${lastError ? lastError.message : "unknown"}`);
      while (true) {
        try {
          const postData = JSON.stringify({
            model: "llama-3.1-8b-instant",
            messages: [
              { role: "system", content: (systemPrompts[persona]?.[lang] || systemPrompts[persona]?.['en'] || "You are a lead.") + "\nInstruction: DO NOT summarize or repeat the agent's points. Remember previous answers and do not ask redundant questions. Be direct and concise." + introContext },
              ...groqMessages
            ],
            temperature: 0.5, 
            max_tokens: 1024,
          });

          const response = await new Promise((resolve, reject) => {
            const options = {
              hostname: 'api.groq.com',
              path: '/openai/v1/chat/completions',
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
                'Content-Length': Buffer.byteLength(postData)
              }
            };

            const req = https.request(options, (res) => {
              res.setEncoding('utf8');
              let body = '';
              res.on('data', (chunk) => body += chunk);
              res.on('end', () => resolve({ status: res.statusCode, data: body }));
            });

            req.on('error', (e) => reject(e));
            req.write(postData);
            req.end();
          });

          const groqData = JSON.parse(response.data);
          if (response.status === 200) {
            finalCompletion = groqData;
            console.log("Emergency loop recovered successfully!");
            break;
          }
        } catch (e) {
          console.log(`Emergency loop failed: ${e.message}. Retrying in 3 seconds...`);
          await delay(3000);
        }
      }
    }

    return {
      statusCode: 200,
      body: JSON.stringify({ 
        message: finalCompletion.choices[0].message.content,
        version: "v5.1-Stable" 
      })
    };

  } catch (error) {
    return { 
      statusCode: 500, 
      body: JSON.stringify({ 
        error: error.message, 
        version: "v5.1-Stable" 
      }) 
    };
  }
};
