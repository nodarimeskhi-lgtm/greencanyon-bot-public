exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }

  try {
    const logData = JSON.parse(event.body);
    const scriptUrl = process.env.GOOGLE_SCRIPT_URL;

    if (!scriptUrl) {
      console.warn('GOOGLE_SCRIPT_URL not set, skipping remote logging.');
      return { statusCode: 200, body: JSON.stringify({ status: 'skipped' }) };
    }

    const response = await fetch(scriptUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(logData)
    });

    return {
      statusCode: 200,
      body: JSON.stringify({ status: 'success' })
    };
  } catch (error) {
    console.error('Logging error:', error);
    return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
  }
};
