import express from "express";
import cors from "cors";
import sessionRoutes from "./routes/sessionRoutes.js";
import chatRoutes from "./routes/chatRoutes.js";
import quizRoutes from "./routes/quizRoutes.js";
import exportRoutes from "./routes/exportRoutes.js";

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/session", sessionRoutes);
app.use("/api/chat", chatRoutes);
app.use("/api/quiz", quizRoutes);
app.use("/api/export", exportRoutes);

app.get("/", (req, res) => {
    res.send("Backend is running");
})

// Global error handler
app.use((err, req, res, next) => {
    console.error(err);
    res.status(err.status || 500).json({ error: err.message || 'Internal Server Error' });
});

export default app;