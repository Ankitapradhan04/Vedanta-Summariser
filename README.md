# 🕉️ Vedanta Summarizer

**A 100% free AI-powered web app that decodes ancient Sanskrit manuscripts**

Upload an image of a Sanskrit manuscript → get extracted Sanskrit text, English translation, and a Vedantic summary — all using free tools, no paid APIs.

---

## ✨ Features & Free Technologies

| Feature | Technology | Cost |
|---|---|---|
| 📜 Sanskrit OCR | Tesseract OCR + Sanskrit language pack | Free / Open-source |
| 🖼️ Image enhancement | OpenCV (denoising, thresholding, upscaling) | Free / Open-source |
| 🔤 Devanagari rendering | Google Fonts — Noto Sans Devanagari | Free |
| 🌐 Translation (no token) | MyMemory REST API | Free, no signup |
| 🌐 Translation (with token) | HuggingFace Helsinki-NLP opus-mt-sa-en | Free HF account |
| ✨ AI Summary (with token) | HuggingFace facebook/bart-large-cnn | Free HF account |
| ✨ Summary (no token) | Extractive sentence-ranking | No API needed |

---

## 🏗️ Project Structure

```
vedanta_summarizer/
├── app.py                  # Flask backend
├── requirements.txt        # Python dependencies
├── README.md
├── .gitignore
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── uploads/                # Temp storage (auto-created)
```

---
