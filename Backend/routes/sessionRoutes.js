import express from "express";
import { createSession } from "../controllers/sessionControllers.js";

const router = express.Router();

router.post("/create", createSession);

export default router;
