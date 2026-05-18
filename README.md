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

## 🚀 Setup & Running in VS Code

### Step 1 — Install Tesseract OCR

**Windows:**
1. Download from https://github.com/UB-Mannheim/tesseract/wiki
2. During install, tick ✅ Additional script data → ✅ **Sanskrit**
3. Add `C:\Program Files\Tesseract-OCR` to your system PATH

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Ubuntu / Debian:**
```bash
sudo apt-get update && sudo apt-get install tesseract-ocr tesseract-ocr-san
```

Verify:
```bash
tesseract --list-langs   # 'san' should appear
```

---

### Step 2 — Clone / Open in VS Code

```bash
git clone https://github.com/YOUR_USERNAME/vedanta-summarizer.git
cd vedanta-summarizer
code .
```

---

### Step 3 — Create a Virtual Environment

Open VS Code Terminal (`Ctrl+\``) and run:

```bash
# Create venv
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
```

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Run

```bash
python app.py
```

Open **http://localhost:5000** in your browser.

---

## 🤗 Optional: Free HuggingFace Token (Better Results)

Without a token the app still works fully (Tesseract + MyMemory).  
A free HuggingFace token unlocks two extra AI models:

1. Go to https://huggingface.co → sign up free
2. Settings → Access Tokens → **New token** (read role is enough)
3. Copy the token (`hf_...`) and paste it into the app's token field

Models used (both free on HF Inference API):
- `Helsinki-NLP/opus-mt-sa-en` — Sanskrit → English neural translation
- `facebook/bart-large-cnn` — Abstractive summarization

---

## 📤 Pushing to GitHub

### 1. Create a GitHub repo
Go to https://github.com → New repository → name it `vedanta-summarizer` → **don't** init with README.

### 2. Push from VS Code terminal

```bash
git init
git add .
git commit -m "Initial commit: Vedanta Summarizer"
git remote add origin https://github.com/YOUR_USERNAME/vedanta-summarizer.git
git branch -M main
git push -u origin main
```

### 3. Future updates

```bash
git add .
git commit -m "describe your change"
git push
```

---

## 🌐 Free Deployment (Render)

1. Go to https://render.com → sign in with GitHub
2. New → Web Service → connect your repo
3. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
4. Add `gunicorn` to requirements.txt first:
   ```bash
   echo "gunicorn>=20.1.0" >> requirements.txt
   ```

> **Note:** Cloud deployments need Tesseract installed in the build environment.  
> Add a `render.yaml` or use a `Dockerfile` with `RUN apt-get install -y tesseract-ocr tesseract-ocr-san`.

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `tesseract is not installed` | Install Tesseract and add it to PATH |
| `san language data not found` | Re-run installer with Sanskrit option checked |
| Translation returns odd text | Normal for degraded manuscripts; add a HF token for better results |
| `Port 5000 in use` | Change `port=5000` to `port=5001` in app.py |
| HF model returns 503 | Model is loading — the app auto-retries after 20 s |

---

## 📝 Supported Image Formats

PNG · JPG · JPEG · TIFF · WebP · GIF · BMP (up to 16 MB)

**Best results:** 300+ DPI scans, clear Devanagari script, good contrast

---

*"सर्वे भवन्तु सुखिनः" — May all beings be happy*
