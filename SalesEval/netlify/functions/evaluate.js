const https = require('https');

exports.handler = async (event, context) => {
  const apiKey = process.env.GROQ_API_KEY;

  if (!apiKey) {
    return { statusCode: 500, body: JSON.stringify({ error: "API key missing" }) };
  }

  try {
    const { history, persona, lang } = JSON.parse(event.body);

    const evalPrompt = `
      Evaluate the agent's performance in this sales conversation (Lead: ${persona}).
      Target: Green Canyon (Tsalka, ROI 8-12%, Escrow).
      
      Conversation:
      ${(history || []).slice(-10).map(m => `${m.type}: ${m.text}`).join('\n')}
      
      Return RAW JSON only:
      {
        "score": number (0-10),
        "accuracy": number (0-100),
        "objection": number (0-100),
        "softSkills": number (0-100),
        "feedback": ["feedback in ${lang === 'ka' ? 'Georgian' : 'English'}", ...]
      }
    `;

    const postData = JSON.stringify({
      model: "llama-3.1-8b-instant",
      messages: [
        { role: "system", content: "Return RAW JSON only." },
        { role: "user", content: evalPrompt }
      ],
      temperature: 0.1,
      response_format: { type: "json_object" }
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

    try {
      const groqData = JSON.parse(response.data);
      
      if (response.status !== 200) {
        return { 
          statusCode: response.status, 
          body: JSON.stringify({ 
            error: groqData.error?.message || "Groq issue", 
            version: "v5.1-Stable", 
            modelUsed: "llama-3.1-8b-instant" 
          }) 
        };
      }

      let cleanJson = groqData.choices[0].message.content.trim();
      if (cleanJson.includes('```')) {
        cleanJson = cleanJson.replace(/```json/g, '').replace(/```/g, '').trim();
      }

      const parsedResult = JSON.parse(cleanJson);
      // Adding version to successful response for debug
      parsedResult._version = "v5.1-Stable";

      return {
        statusCode: 200,
        body: JSON.stringify(parsedResult)
      };
    } catch (e) {
      return { 
        statusCode: 500, 
        body: JSON.stringify({ 
          error: "Parse error", 
          debug: response.data.substring(0, 100),
          version: "v5.1-Stable" 
        }) 
      };
    }

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
