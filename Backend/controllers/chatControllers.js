import {askRagQuestion} from "../services/aiclientService.js";

export const askQuestion = async (req, res) => {
    try {
        const { sessionId, question } = req.body;
        if (!sessionId || !question) return res.status(400).json({ error: 'sessionId and question are required' });

        const answer = await askRagQuestion(sessionId, question);
        return res.json(answer);
    } catch (err) {
        return res.status(500).json({ error: err.message || 'Failed to get answer' });
    }
};