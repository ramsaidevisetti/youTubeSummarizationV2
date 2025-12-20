import OpenAI from "openai";

let openaiClient = null;
function getOpenAI() {
  if (openaiClient) return openaiClient;
  const apiKey = process.env.OPENAI_API_KEY;
  if (!apiKey) return null;
  openaiClient = new OpenAI({ apiKey });
  return openaiClient;
}

export const createQuiz = async () => {
  const openai = getOpenAI();
  if (!openai) {
    throw new Error('OPENAI_API_KEY not set. Set the environment variable or provide a .env file.');
  }

  const response = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [
      { role: "user", content: "Generate 5 MCQs from the lecture." }
    ]
  });

  return { quiz: response.choices[0].message.content };
};

export const evaluateAnswers = async (sessionId, answers) => {
  return {
    score: answers.length,
    feedback: "Good attempt!"
  };
};
