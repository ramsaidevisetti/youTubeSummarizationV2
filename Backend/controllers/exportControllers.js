import {generatePDF} from "../services/pdfService.js"

export const exportPDF = async (req, res) => {
    try {
        const sessionId = req.params.sessionId || req.body.sessionId;
        if (!sessionId) return res.status(400).json({ error: 'sessionId is required' });

        const pdf = await generatePDF(sessionId);
        return res.download(pdf);
    } catch (err) {
        return res.status(500).json({ error: err.message || 'Failed to generate PDF' });
    }
}