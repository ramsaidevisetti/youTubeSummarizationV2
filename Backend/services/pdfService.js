import PDFDocument from "pdfkit";
import fs from "fs";

export const generatePDF = async (sessionId) => {
  const doc = new PDFDocument();
  const path = `storage/reports/${sessionId}.pdf`;

  doc.pipe(fs.createWriteStream(path));
  doc.text("YouTube Study Assistant Report");
  doc.text(`Session ID: ${sessionId}`);
  doc.end();

  return path;
};
