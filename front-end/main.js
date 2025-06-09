// Caching
let lastText = '';
let lastAudioUrl = '';
let isLoading = false;
// Language dictionary
const dict = {
  en: {
    title: "Bahnar Text-To-Speech",
    enterText: "Enter text here",
    speak: "Speak",
    upload: "Upload Text File",
    history: "History",
    navText: "Text-to-speech",
    navPicture: "Image-to-speech"
  },
  vi: {
    title: "Chuyển Văn Bản Thành Giọng Nói Bahnar",
    enterText: "Nhập văn bản tại đây",
    speak: "Đọc",
    upload: "Tải tệp văn bản",
    history: "Lịch sử",
    navText: "Chuyển văn bản thành giọng nói",
    navPicture: "Chuyển ảnh thành giọng nói"
  }
};
let currentLang = 'en';

function setLang(lang) {
  currentLang = lang;
  document.getElementById('app-title').innerText = dict[lang].title;
  document.getElementById('text-label').innerText = dict[lang].enterText;
  document.getElementById('text').placeholder = dict[lang].enterText;
  document.getElementById('speak-btn-text').innerText = dict[lang].speak;
  document.getElementById('upload-btn-text').innerText = dict[lang].upload;
  document.getElementById('history-title').innerText = dict[lang].history;
  document.getElementById('nav-text-label').innerText = dict[lang].navText;
  document.getElementById('nav-picture-label').innerText = dict[lang].navPicture;
  document.documentElement.lang = lang;
}
function changeLang() {
  const lang = document.getElementById('lang-select').value;
  setLang(lang);
}
// Initial language
setLang('en');

async function speak() {
  if (isLoading) return;
  const text = document.getElementById('text').value.trim();
  if (!text) return;
  const audioElem = document.getElementById('audio');
  // If same text, replay cached audio
  if (text === lastText && lastAudioUrl) {
    audioElem.src = lastAudioUrl;
    audioElem.currentTime = 0;
    audioElem.play();
    addToHistory(text, lastAudioUrl);
    return;
  }
  isLoading = true;
  setSpeakLoading(true);
  const gender = "male";
  try {
    const response = await fetch('http://localhost:5000/speak', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, gender })
    });
    const data = await response.json();
    const audioData = data.speech;
    const binary = atob(audioData);
    const array = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) {
      array[i] = binary.charCodeAt(i);
    }
    const blob = new Blob([array], { type: 'audio/wav' });
    const url = URL.createObjectURL(blob);
    audioElem.src = url;
    audioElem.currentTime = 0;
    audioElem.play();
    // Cache
    lastText = text;
    lastAudioUrl = url;
    addToHistory(text, url);
  } catch (e) {
    lastText = '';
    lastAudioUrl = '';
    alert('Error generating speech.');
  }
  setSpeakLoading(false);
  isLoading = false;
}

function setSpeakLoading(loading) {
  const btn = document.getElementById('speak-btn');
  const btnText = document.getElementById('speak-btn-text');
  if (loading) {
    btn.setAttribute('disabled', 'disabled');
    btnText.innerHTML = '<span class="spinner"></span>';
  } else {
    btn.removeAttribute('disabled');
    btnText.innerText = dict[currentLang].speak;
  }
}

function uploadTextFile(event) {
  const file = event.target.files[0];
  if (!file) return;
  const ext = file.name.split('.').pop().toLowerCase();
  if (ext === "txt") {
    const reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('text').value = e.target.result;
      autoGrow(document.getElementById('text'));
    };
    reader.readAsText(file, 'UTF-8');
  } else if (ext === "docx") {
    // Requires mammoth.browser.min.js included in HTML
    const reader = new FileReader();
    reader.onload = function(e) {
      mammoth.extractRawText({arrayBuffer: e.target.result})
        .then(function(result){
          document.getElementById('text').value = result.value;
          autoGrow(document.getElementById('text'));
        })
        .catch(function(err){
          alert('Failed to read .docx file.');
        });
    };
    reader.readAsArrayBuffer(file);
  } else if (ext === "doc") {
    alert('Reading .doc files is not supported. Please use .txt or .docx.');
  } else {
    alert('Please upload a .txt, .doc, or .docx file.');
  }
  // Reset file input so same file can be uploaded again if needed
  event.target.value = '';
}

function autoGrow(element) {
  element.style.height = "auto";
  element.style.height = (element.scrollHeight) + "px";
}

// History logic
let history = [];
function addToHistory(text, audioUrl) {
  // Remove any previous entry with the same text
  history = history.filter(item => item.text !== text);
  // Add new entry to the top
  history.unshift({ text, audioUrl, time: new Date().toLocaleTimeString() });
  if (history.length > 20) history.pop();
  renderHistory();
}
function renderHistory() {
  const list = document.getElementById('history-list');
  list.innerHTML = '';
  history.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'history-item';
    const textDiv = document.createElement('div');
    textDiv.className = 'history-text';
    textDiv.textContent = item.text.length > 80 ? item.text.slice(0, 80) + '...' : item.text;
    const controls = document.createElement('div');
    controls.className = 'history-controls';
    // Play icon
    const playBtn = document.createElement('button');
    playBtn.className = 'icon-btn';
    playBtn.title = 'Play';
    playBtn.innerHTML = '<svg width="22" height="22" viewBox="0 0 22 22"><polygon points="6,4 18,11 6,18" fill="#2563eb"/></svg>';
    playBtn.onclick = () => {
      const audio = new Audio(item.audioUrl);
      audio.play();
    };
    // Download icon
    const downloadBtn = document.createElement('a');
    downloadBtn.className = 'icon-btn';
    downloadBtn.title = 'Download';
    downloadBtn.innerHTML = '<svg width="22" height="22" viewBox="0 0 22 22"><path d="M11 4v9m0 0l-4-4m4 4l4-4M4 18h14" stroke="#2563eb" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>';
    downloadBtn.href = item.audioUrl;
    downloadBtn.download = 'tts.wav';
    controls.appendChild(playBtn);
    controls.appendChild(downloadBtn);
    div.appendChild(textDiv);
    div.appendChild(controls);
    list.appendChild(div);
  });
}

function switchFuncTab(tab) {
  const textGroup = document.getElementById('text-func-group');
  const picGroup = document.getElementById('picture-func-group');
  const navText = document.getElementById('nav-text-btn');
  const navPic = document.getElementById('nav-picture-btn');
  const underline = document.querySelector('.underline'); 
  let activeBtn;

  if (tab === 'text') {
    textGroup.style.display = '';
    picGroup.style.display = 'none';
    navText.classList.add('active');
    navPic.classList.remove('active');
    activeBtn = navText;
  } else {
    textGroup.style.display = 'none';
    picGroup.style.display = '';
    navText.classList.remove('active');
    navPic.classList.add('active');
    activeBtn = navPic;
  }

  
  if (activeBtn && underline) {
    const parentRect = activeBtn.parentElement.getBoundingClientRect();
    const btnRect = activeBtn.getBoundingClientRect();

    const leftPos = btnRect.left - parentRect.left;
    const width = btnRect.width;

    underline.style.left = leftPos + 'px';
    underline.style.width = width + 'px';
  }
}


window.onload = () => {
  switchFuncTab('text');
};

