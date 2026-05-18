import os
import re
import time
import requests
from flask import Flask, request, jsonify, render_template, send_from_directory
from PIL import Image
import pytesseract
import cv2
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}
os.makedirs('uploads', exist_ok=True)

HF_API_TRANSLATE = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-sa-en"
HF_API_SUMMARIZE = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return image_path
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, h=30)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    h, w = thresh.shape
    if w < 1200:
        scale = 1200 / w
        thresh = cv2.resize(thresh, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)
    processed_path = image_path.rsplit('.', 1)[0] + '_processed.png'
    cv2.imwrite(processed_path, thresh)
    return processed_path


def extract_text_tesseract(image_path):
    processed = preprocess_image(image_path)
    img = Image.open(processed)
    for lang, label in [('san', 'Sanskrit'), ('hin', 'Hindi/Devanagari'), ('eng', 'English')]:
        try:
            text = pytesseract.image_to_string(img, config=f'--oem 1 --psm 6 -l {lang}').strip()
            if text:
                return text, f'Tesseract OCR ({label})'
        except Exception:
            continue
    return '', 'Tesseract OCR (no text found)'


def translate_mymemory(text, src='sa', tgt='en'):
    def _chunk(chunk):
        try:
            r = requests.get(
                'https://api.mymemory.translated.net/get',
                params={'q': chunk, 'langpair': f'{src}|{tgt}'},
                timeout=15
            )
            d = r.json()
            if d.get('responseStatus') == 200:
                return d['responseData']['translatedText']
        except Exception:
            pass
        return ''

    words, chunk, chunks, length = text.split(), [], [], 0
    for w in words:
        if length + len(w) + 1 > 450:
            chunks.append(' '.join(chunk))
            chunk, length = [w], len(w)
        else:
            chunk.append(w); length += len(w) + 1
    if chunk:
        chunks.append(' '.join(chunk))
    translated = [_chunk(c) for c in chunks if c.strip()]
    return ' '.join(t for t in translated if t), 'MyMemory API (free, no key needed)'


def translate_huggingface(text, hf_token):
    headers = {'Authorization': f'Bearer {hf_token}'}
    sentences = re.split(r'[।॥\n]+', text)
    parts, buf = [], ''
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        if len(buf) + len(s) + 2 > 512:
            parts.append(buf.strip()); buf = s
        else:
            buf = (buf + ' ' + s).strip()
    if buf:
        parts.append(buf)

    results = []
    for part in parts:
        try:
            r = requests.post(HF_API_TRANSLATE, headers=headers, json={'inputs': part}, timeout=30)
            if r.status_code == 503:
                time.sleep(20)
                r = requests.post(HF_API_TRANSLATE, headers=headers, json={'inputs': part}, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if isinstance(data, list) and data:
                    results.append(data[0].get('translation_text', ''))
        except Exception:
            pass
    if results:
        return ' '.join(results), 'HuggingFace Helsinki-NLP opus-mt-sa-en (free)'
    return None, 'HuggingFace translation failed'


def summarize_huggingface(text, hf_token):
    headers = {'Authorization': f'Bearer {hf_token}'}
    trimmed = text[:3000]
    try:
        r = requests.post(
            HF_API_SUMMARIZE, headers=headers,
            json={'inputs': trimmed, 'parameters': {'max_length': 300, 'min_length': 80, 'do_sample': False}},
            timeout=60
        )
        if r.status_code == 503:
            time.sleep(20)
            r = requests.post(HF_API_SUMMARIZE, headers=headers,
                              json={'inputs': trimmed, 'parameters': {'max_length': 300, 'min_length': 80}},
                              timeout=60)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, list) and data:
                return data[0].get('summary_text', ''), 'facebook/bart-large-cnn (free HuggingFace)'
    except Exception as e:
        return None, str(e)
    return None, 'HuggingFace summarization failed'


def summarize_extractive(text):
    sentences = re.split(r'[.!?।॥]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if len(sentences) <= 3:
        return text, 'Extractive (short text)'
    words = re.findall(r'\w+', text.lower())
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    scores = [(sum(freq.get(w.lower(), 0) for w in re.findall(r'\w+', s)), s) for s in sentences]
    scores.sort(reverse=True)
    top = {s for _, s in scores[:3]}
    ordered = [s for s in sentences if s in top]
    return '. '.join(ordered) + '.', 'Extractive summary (no API required)'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_manuscript():
    result = {
        'success': False, 'sanskrit_text': '', 'english_translation': '',
        'summary': '', 'ocr_method': '', 'translation_method': '',
        'summary_method': '', 'errors': []
    }

    hf_token = request.form.get('hf_token', '').strip()

    if 'image' not in request.files:
        result['errors'].append('No image file uploaded.')
        return jsonify(result), 400

    file = request.files['image']
    if file.filename == '' or not allowed_file(file.filename):
        result['errors'].append('Invalid or missing file.')
        return jsonify(result), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Step 1: OCR
    sanskrit_text, ocr_method = extract_text_tesseract(filepath)
    result['ocr_method'] = ocr_method
    if not sanskrit_text:
        result['errors'].append('Could not extract text. Try a higher-resolution image.')
        return jsonify(result), 422
    result['sanskrit_text'] = sanskrit_text

    # Step 2: Translation — HF if token given, else MyMemory
    english_text = None
    if hf_token:
        english_text, trans_method = translate_huggingface(sanskrit_text, hf_token)
    if not english_text:
        english_text, trans_method = translate_mymemory(sanskrit_text)
    result['english_translation'] = english_text or '[Translation unavailable]'
    result['translation_method'] = trans_method

    # Step 3: Summary — HF BART if token given, else extractive
    summary = None
    source = english_text or sanskrit_text
    if hf_token and source:
        summary, sum_method = summarize_huggingface(source, hf_token)
    if not summary:
        summary, sum_method = summarize_extractive(source or '')
    result['summary'] = summary or 'Summary could not be generated.'
    result['summary_method'] = sum_method
    result['success'] = True

    processed = filepath.rsplit('.', 1)[0] + '_processed.png'
    if os.path.exists(processed):
        os.remove(processed)

    return jsonify(result)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
