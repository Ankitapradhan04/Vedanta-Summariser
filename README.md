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

<img width="705" height="387" alt="image" src="https://github.com/user-attachments/assets/6beb1f94-624a-4ae2-858d-fcc11839205c" />

<img width="712" height="542" alt="image" src="https://github.com/user-attachments/assets/23e4ff3b-4d80-4070-b41d-9fe7d6ae21a3" />

<img width="703" height="435" alt="Screenshot 2026-05-22 at 1 09 24 PM" src="https://github.com/user-attachments/assets/6f931cf5-7c2a-4daf-8a2b-158fc6cf16f3" />

<img width="709" height="571" alt="Screenshot 2026-05-22 at 1 09 45 PM" src="https://github.com/user-attachments/assets/20342cff-c81e-4b63-b78c-72b78c0529c7" />
