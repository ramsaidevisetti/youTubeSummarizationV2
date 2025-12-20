import express from "express";
import { askQuestion } from "../controllers/chatControllers.js";

const router = express.Router();

router.post("/ask", askQuestion);

export default router;
