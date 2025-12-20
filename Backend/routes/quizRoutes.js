import express from "express"
import {generateQuiz, evaluateQuiz} from "../controllers/quizControllers.js";

const router = express.Router();
router.post("/generate",generateQuiz);
router.post("/evaluate",evaluateQuiz);

export default router;