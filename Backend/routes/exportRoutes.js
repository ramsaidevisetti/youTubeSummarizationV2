import express from "express"
import {exportPDF} from "../controllers/exportControllers.js";

const router = express.Router();
router.get("/pdf/:sessionId",exportPDF);

export default router;