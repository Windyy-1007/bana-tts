// Requires tesseract.min.js loaded via CDN or local file

// Setup drag and drop
const dropArea = document.getElementById('image-drop-area');
const ocrResult = document.getElementById('ocr-result');
const speakOcrBtn = document.getElementById('speak-ocr-btn');
const speakOcrBtnText = document.getElementById('speak-ocr-btn-text');
const uploadImageBtnText = document.getElementById('upload-image-btn-text');
const ocrAudio = document.getElementById('ocr-audio');
const imageUpload = document.getElementById('image-upload');
const imageDropMsg = document.getElementById('image-drop-msg');

let ocrText = '';
let ocrAudioUrl = '';
let ocrIsLoading = false;

function setOcrLang(lang) {
  // Optionally update drop message and button text for i18n
  if (lang === 'vi') {
    imageDropMsg.innerText = 'Kéo và thả ảnh vào đây';
    uploadImageBtnText.innerText = 'Tải ảnh lên';
    speakOcrBtnText.innerText = 'Đọc';
    ocrResult.placeholder = 'Kết quả OCR sẽ hiển thị ở đây';
  } else {
    imageDropMsg.innerText = 'Drag and drop an image here';
    uploadImageBtnText.innerText = 'Upload Image';
    speakOcrBtnText.innerText = 'Speak';
    ocrResult.placeholder = 'OCR result will appear here';
  }
}
if (typeof currentLang !== 'undefined') setOcrLang(currentLang);

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (file) {
    processImageFile(file);
  }
  event.target.value = '';
}

dropArea.addEventListener('click', () => imageUpload.click());
dropArea.addEventListener('dragover', e => {
  e.preventDefault();
  dropArea.classList.add('dragover');
});
dropArea.addEventListener('dragleave', e => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
});
dropArea.addEventListener('drop', e => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
  if (e.dataTransfer.files && e.dataTransfer.files[0]) {
    processImageFile(e.dataTransfer.files[0]);
  }
});

function processImageFile(file) {
  ocrResult.value = '';
  speakOcrBtn.disabled = true;
  ocrText = '';
  ocrAudioUrl = '';
  ocrResult.placeholder = 'Processing...';
  Tesseract.recognize(
    file,
    'eng+vie', // English + Vietnamese
    { logger: m => { /* Optionally handle progress */ } }
  ).then(({ data: { text } }) => {
    ocrText = text.trim();
    ocrResult.value = ocrText;
    ocrResult.placeholder = '';
    speakOcrBtn.disabled = !ocrText;
  }).catch(() => {
    ocrResult.value = '';
    ocrResult.placeholder = 'OCR failed. Please try another image.';
    speakOcrBtn.disabled = true;
  });
}

function speakOcr() {
  if (!ocrText) return;
  if (ocrAudioUrl) {
    ocrAudio.src = ocrAudioUrl;
    ocrAudio.currentTime = 0;
    ocrAudio.play();
    return;
  }
  speakOcrBtn.disabled = true;
  speakOcrBtnText.innerHTML = '<span class="spinner"></span>';
  fetch('http://localhost:5000/speak', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: ocrText, gender: "male" })
  })
    .then(res => res.json())
    .then(data => {
      const audioData = data.speech;
      const binary = atob(audioData);
      const array = new Uint8Array(binary.length);
      for (let i = 0; i < binary.length; i++) {
        array[i] = binary.charCodeAt(i);
      }
      const blob = new Blob([array], { type: 'audio/wav' });
      const url = URL.createObjectURL(blob);
      ocrAudio.src = url;
      ocrAudioUrl = url;
      ocrAudio.currentTime = 0;
      ocrAudio.play();
    })
    .catch(() => {
      alert('Error generating speech.');
    })
    .finally(() => {
      speakOcrBtn.disabled = false;
      speakOcrBtnText.innerText = (typeof currentLang !== 'undefined' && currentLang === 'vi') ? 'Đọc' : 'Speak';
    });
}

// Optional: update OCR UI language when switching
if (typeof setLang === 'function') {
  const origSetLang = setLang;
  window.setLang = function(lang) {
    origSetLang(lang);
    setOcrLang(lang);
  };
}
