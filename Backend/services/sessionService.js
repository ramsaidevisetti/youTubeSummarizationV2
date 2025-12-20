import { v4 as uuid } from "uuid";

export const createNewSession = async (youtubeUrl) => {
  return {
    sessionId: uuid(),
    youtubeUrl,
    status: "READY"
  };
};
