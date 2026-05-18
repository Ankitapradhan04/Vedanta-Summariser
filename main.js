// Vedanta Summarizer — Main JavaScript

let selectedFile = null;

// ---- File Input & Drag/Drop ----

document.getElementById('imageInput').addEventListener('change', function (e) {
    const file = e.target.files[0];
    if (file) handleFile(file);
});

const uploadArea = document.getElementById('uploadArea');

uploadArea.addEventListener('click', () => {
    document.getElementById('imageInput').click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('drag-over');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file && isImage(file)) {
        handleFile(file);
    } else {
        showToast('Please drop an image file.');
    }
});

function isImage(file) {
    return file.type.startsWith('image/');
}

function handleFile(file) {
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        document.getElementById('imagePreview').src = e.target.result;
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('previewContainer').style.display = 'block';
        document.getElementById('uploadArea').style.display = 'none';
        document.getElementById('processBtn').disabled = false;
    };
    reader.readAsDataURL(file);
}

function removeImage() {
    selectedFile = null;
    document.getElementById('imageInput').value = '';
    document.getElementById('previewContainer').style.display = 'none';
    document.getElementById('uploadArea').style.display = 'block';
    document.getElementById('processBtn').disabled = true;
    hideResults();
}

// ---- Processing ----

async function processManuscript() {
    if (!selectedFile) {
        showToast('Please select an image first.');
        return;
    }

    showProcessing(true);
    hideResults();
    animateSteps();

    const formData = new FormData();
    formData.append('image', selectedFile);

    const hfToken = document.getElementById('hfToken').value.trim();
    if (hfToken) formData.append('hf_token', hfToken);

    try {
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        showProcessing(false);

        if (!response.ok || !data.success) {
            displayErrors(data.errors || ['An error occurred processing the image.']);
        } else {
            displayResults(data);
        }
    } catch (err) {
        showProcessing(false);
        displayErrors(['Network error: ' + err.message]);
    }
}

// ---- Display Results ----

function displayResults(data) {
    // Sanskrit Text
    const sanskritEl = document.getElementById('sanskritText');
    if (data.sanskrit_text) {
        sanskritEl.textContent = data.sanskrit_text;
        document.getElementById('ocrMethod').textContent = data.ocr_method;
    } else {
        document.getElementById('sanskritCard').style.display = 'none';
    }

    // English Translation
    const englishEl = document.getElementById('englishText');
    if (data.english_translation) {
        englishEl.textContent = data.english_translation;
        document.getElementById('transMethod').textContent = data.translation_method;
    } else {
        document.getElementById('translationCard').style.display = 'none';
    }

    // Summary
    const summaryEl = document.getElementById('summaryText');
    if (data.summary) {
        // Render markdown-style bold/headers
        summaryEl.innerHTML = formatSummary(data.summary);
        document.getElementById('sumMethod').textContent = data.summary_method;
    } else {
        document.getElementById('summaryCard').style.display = 'none';
    }

    // Errors
    if (data.errors && data.errors.length > 0) {
        displayErrors(data.errors);
    }

    document.getElementById('resultsSection').style.display = 'block';

    // Scroll to results
    setTimeout(() => {
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 300);
}

function formatSummary(text) {
    // Convert **bold** to <strong>
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Convert numbered headings like "1. **Title**:" 
    text = text.replace(/(\d+\.\s*<strong>.*?<\/strong>)/g, '<br>$1');
    // Convert line breaks
    text = text.replace(/\n/g, '<br>');
    return text;
}

function displayErrors(errors) {
    const errorCard = document.getElementById('errorCard');
    const errorList = document.getElementById('errorList');
    errorList.innerHTML = '';
    errors.forEach(err => {
        const li = document.createElement('li');
        li.textContent = err;
        errorList.appendChild(li);
    });
    errorCard.style.display = 'block';
    document.getElementById('resultsSection').style.display = 'block';
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
    document.getElementById('errorCard').style.display = 'none';
    ['sanskritCard', 'translationCard', 'summaryCard'].forEach(id => {
        document.getElementById(id).style.display = 'block';
    });
}

// ---- Processing Animation ----

let stepInterval = null;

function animateSteps() {
    const steps = ['step1', 'step2', 'step3', 'step4'];
    let i = 0;
    // Reset all
    steps.forEach(s => {
        const el = document.getElementById(s);
        el.classList.remove('active', 'done');
    });

    document.getElementById(steps[0]).classList.add('active');

    stepInterval = setInterval(() => {
        if (i < steps.length - 1) {
            document.getElementById(steps[i]).classList.remove('active');
            document.getElementById(steps[i]).classList.add('done');
            i++;
            document.getElementById(steps[i]).classList.add('active');
        }
    }, 2500);
}

function showProcessing(show) {
    const overlay = document.getElementById('processingOverlay');
    overlay.style.display = show ? 'flex' : 'none';
    if (!show && stepInterval) {
        clearInterval(stepInterval);
        stepInterval = null;
    }
}

// ---- Copy ----

function copyText(elementId) {
    const el = document.getElementById(elementId);
    const text = el.innerText || el.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!');
    }).catch(() => {
        // Fallback
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        showToast('Copied!');
    });
}

// ---- Export Report ----

function exportReport() {
    const sanskrit = document.getElementById('sanskritText').textContent || '';
    const english = document.getElementById('englishText').textContent || '';
    const summary = document.getElementById('summaryText').innerText || '';

    const date = new Date().toLocaleDateString('en-IN', {
        year: 'numeric', month: 'long', day: 'numeric'
    });

    const report = `VEDANTA SUMMARIZER — MANUSCRIPT REPORT
Generated: ${date}
${'═'.repeat(60)}

I. EXTRACTED SANSKRIT TEXT
${'─'.repeat(60)}
${sanskrit}

II. ENGLISH TRANSLATION
${'─'.repeat(60)}
${english}

III. VEDANTIC SUMMARY
${'─'.repeat(60)}
${summary}

${'═'.repeat(60)}
Generated by Vedanta Summarizer
Powered by Tesseract OCR, MyMemory API & Claude AI
`;

    const blob = new Blob([report], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `vedanta_manuscript_report_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    showToast('Report exported!');
}

// ---- Reset ----

function resetApp() {
    removeImage();
    hideResults();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ---- Toast ----

let toastTimeout;

function showToast(message) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.display = 'block';
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}
