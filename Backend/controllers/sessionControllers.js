import { createNewSession } from "../services/sessionService.js";

export const createSession = async (req, res) => {
  try {
    const { youtubeUrl } = req.body;
    if (!youtubeUrl) return res.status(400).json({ error: 'youtubeUrl is required' });

    const session = await createNewSession(youtubeUrl);
    return res.json(session);
  } catch (err) {
    return res.status(500).json({ error: err.message || 'Failed to create session' });
  }
};

