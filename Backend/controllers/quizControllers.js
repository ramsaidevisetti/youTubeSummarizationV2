import {createQuiz, evaluateAnswers} from "../services/quizService.js";

export const generateQuiz = async(req, res) => {
    try {
        const { sessionId } = req.body;
        if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

        const quiz  = await createQuiz(sessionId);
        return res.json(quiz);
    } catch (err) {
        return res.status(500).json({ error: err.message || 'Failed to generate quiz' });
    }
}

export const evaluateQuiz = async(req, res) => {
    try {
        const { sessionId, answer } = req.body;
        if (!sessionId || !answer) return res.status(400).json({ error: 'sessionId and answer are required' });

        const result = await evaluateAnswers(sessionId, answer);
        return res.json(result);
    } catch (err) {
        return res.status(500).json({ error: err.message || 'Failed to evaluate answers' });
    }
};