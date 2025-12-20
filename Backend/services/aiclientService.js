import OpenAI from "openai";

let openaiClient = null;

function getOpenAI() {
  if (openaiClient) return openaiClient;
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return null;
  openaiClient = new OpenAI({ apiKey });
  return openaiClient;
}

export const askRagQuestion = async (sessionId, question) => {
  const openai = getOpenAI();
  if (!openai) {
    throw new Error('OPENAI_API_KEY not set. Set the environment variable or provide a .env file.');
  }

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "system", content: "Answer only from video content." },
      { role: "user", content: question }
    ]
  });

  return { answer: response.choices[0].message.content };
};
