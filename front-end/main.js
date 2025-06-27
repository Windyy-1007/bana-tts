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
    navPicture: "Image-to-speech",
    guideTitle: "Typing Guide",
    guideSpecialChars: "Special Characters:",
    guideTips: "Tips:",
    guideTip1: "• Case doesn't matter for 2nd character (Uu → Ŭ)",
    guideTip2: "• Repeat same character to cancel (e66 → e6)",
    guideTip3: "• Type naturally - replacement happens instantly",
    guideTip4: "• Turn off Unikey on laptop/PC or switch to English keyboard on phone"
  },
  vi: {
    title: "Chuyển Văn Bản Thành Giọng Nói Bahnar",
    enterText: "Nhập văn bản tại đây",
    speak: "Đọc",
    upload: "Tải tệp văn bản",
    history: "Lịch sử",
    navText: "Chuyển văn bản thành giọng nói",
    navPicture: "Chuyển ảnh thành giọng nói",
    guideTitle: "Hướng Dẫn Gõ",
    guideSpecialChars: "Ký Tự Đặc Biệt:",
    guideTips: "Mẹo:",
    guideTip1: "• Không phân biệt hoa thường ký tự thứ 2 (Uu → Ŭ)",
    guideTip2: "• Lặp lại ký tự để hủy (e66 → e6)",
    guideTip3: "• Gõ tự nhiên - thay thế ngay lập tức",
    guideTip4: "• Tắt Unikey trên laptop/PC hoặc chuyển sang bàn phím tiếng Anh trên điện thoại"
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
  
  // Update guide elements if they exist
  const guideTitle = document.getElementById('guide-title');
  const guideSpecialChars = document.getElementById('guide-special-chars');
  const guideTips = document.getElementById('guide-tips');
  const guideTip1 = document.getElementById('guide-tip-1');
  const guideTip2 = document.getElementById('guide-tip-2');
  const guideTip3 = document.getElementById('guide-tip-3');
  const guideTip4 = document.getElementById('guide-tip-4');
  
  if (guideTitle) guideTitle.innerText = dict[lang].guideTitle;
  if (guideSpecialChars) guideSpecialChars.innerText = dict[lang].guideSpecialChars;
  if (guideTips) guideTips.innerText = dict[lang].guideTips;
  if (guideTip1) guideTip1.innerText = dict[lang].guideTip1;
  if (guideTip2) guideTip2.innerText = dict[lang].guideTip2;
  if (guideTip3) guideTip3.innerText = dict[lang].guideTip3;
  if (guideTip4) guideTip4.innerText = dict[lang].guideTip4;
  
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

function setUploadLoading(loading) {
  const uploadLabel = document.querySelector('label[for="file-upload"]') || document.querySelector('#file-upload').parentElement;
  const uploadBtnText = document.getElementById('upload-btn-text');
  if (loading) {
    uploadLabel.classList.add('disabled');
    uploadBtnText.innerHTML = '<span class="spinner"></span>';
  } else {
    uploadLabel.classList.remove('disabled');
    uploadBtnText.innerText = dict[currentLang].upload;
  }
}

function uploadTextFile(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  setUploadLoading(true);
  const ext = file.name.split('.').pop().toLowerCase();
  
  if (ext === "txt") {
    const reader = new FileReader();
    reader.onload = function(e) {
      document.getElementById('text').value = e.target.result;
      autoGrow(document.getElementById('text'));
      setUploadLoading(false);
    };
    reader.onerror = function() {
      alert('Failed to read .txt file.');
      setUploadLoading(false);
    };
    reader.readAsText(file, 'UTF-8');
  } else if (ext === "docx") {
    // Check if mammoth is loaded
    if (typeof mammoth === 'undefined') {
      alert('Document processing library not loaded. Please refresh the page and try again.');
      setUploadLoading(false);
      return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
      mammoth.extractRawText({arrayBuffer: e.target.result})
        .then(function(result){
          if (result.value && result.value.trim()) {
            document.getElementById('text').value = result.value;
            autoGrow(document.getElementById('text'));
          } else {
            alert('No text found in the .docx file or the file may be corrupted.');
          }
          setUploadLoading(false);
        })
        .catch(function(err){
          console.error('Mammoth error:', err);
          alert('Failed to read .docx file. The file may be corrupted or incompatible.');
          setUploadLoading(false);
        });
    };
    reader.onerror = function() {
      alert('Failed to read .docx file.');
      setUploadLoading(false);
    };
    reader.readAsArrayBuffer(file);
  } else {
    alert('Please upload a .txt or .docx file.');
    setUploadLoading(false);
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

function updateUnderlinePosition() {
  const activeBtn = document.querySelector('.func-nav-btn.active');
  const underline = document.querySelector('.underline');
  
  if (activeBtn && underline) {
    const parentRect = activeBtn.parentElement.getBoundingClientRect();
    const btnRect = activeBtn.getBoundingClientRect();

    const leftPos = btnRect.left - parentRect.left;
    const width = btnRect.width;

    underline.style.left = leftPos + 'px';
    underline.style.width = width + 'px';
  }
}

function switchFuncTab(tab) {
  const textGroup = document.getElementById('text-func-group');
  const picGroup = document.getElementById('picture-func-group');
  const navText = document.getElementById('nav-text-btn');
  const navPic = document.getElementById('nav-picture-btn');

  if (tab === 'text') {
    textGroup.style.display = '';
    picGroup.style.display = 'none';
    navText.classList.add('active');
    navPic.classList.remove('active');
  } else {
    textGroup.style.display = 'none';
    picGroup.style.display = '';
    navText.classList.remove('active');
    navPic.classList.add('active');
  }

  // Update underline position after DOM changes
  setTimeout(updateUnderlinePosition, 0);
}

function toggleGuide() {
  const guideCard = document.getElementById('guide-card');
  const guideBackdrop = document.getElementById('guide-backdrop');
  if (guideCard && guideBackdrop) {
    guideCard.classList.toggle('show');
    guideBackdrop.classList.toggle('show');
  }
}

// Close guide when clicking outside
document.addEventListener('click', function(event) {
  const guideCard = document.getElementById('guide-card');
  const guideBackdrop = document.getElementById('guide-backdrop');
  const guideToggleBtn = document.getElementById('guide-toggle-btn');
  
  if (guideCard && guideCard.classList.contains('show')) {
    // If click is outside the guide card and not on the toggle button
    if (!guideCard.contains(event.target) && !guideToggleBtn.contains(event.target)) {
      guideCard.classList.remove('show');
      if (guideBackdrop) {
        guideBackdrop.classList.remove('show');
      }
    }
  }
  
  // Also close when clicking on the backdrop itself
  if (guideBackdrop && event.target === guideBackdrop) {
    guideCard.classList.remove('show');
    guideBackdrop.classList.remove('show');
  }
});

window.onload = () => {
  switchFuncTab('text');
  
  // Add resize listener to fix underline position on screen size changes
  window.addEventListener('resize', () => {
    updateUnderlinePosition();
  });
  
  // Add auto-replace functionality to the text input
  const textInput = document.getElementById('text');
  if (textInput) {
    textInput.addEventListener('input', handleAutoReplace);
  }
};

// Auto-replace functionality for Bahnar diacritical characters
const replacements = {
  // u patterns
  'u8': 'ŭ', 'uu': 'ŭ', 'u\\': 'ŭ',
  'U8': 'Ŭ', 'UU': 'Ŭ', 'Uu': 'Ŭ', 'uU': 'Ŭ', 'U\\': 'Ŭ',
  
  // c patterns
  'c6': 'ĉ', 'cc': 'ĉ', 'c\\': 'ĉ',
  'C6': 'Ĉ', 'CC': 'Ĉ', 'Cc': 'Ĉ', 'cC': 'Ĉ', 'C\\': 'Ĉ',
  
  // e patterns
  'e8': 'ĕ', 'ew': 'ĕ', 'e\\': 'ĕ',
  'E8': 'Ĕ', 'EW': 'Ĕ', 'Ew': 'Ĕ', 'eW': 'Ĕ', 'E\\': 'Ĕ',
  
  // i patterns
  'i8': 'ĭ', 'iw': 'ĭ', 'i\\': 'ĭ',
  'I8': 'Ĭ', 'IW': 'Ĭ', 'Iw': 'Ĭ', 'iW': 'Ĭ', 'I\\': 'Ĭ',
  
  // n patterns
  'n4': 'ñ', 'nx': 'ñ', 'n\\': 'ñ',
  'N4': 'Ñ', 'NX': 'Ñ', 'Nx': 'Ñ', 'nX': 'Ñ', 'N\\': 'Ñ',
  
  // o patterns
  'o8': 'ǒ', 'o\\': 'ǒ',
  'O8': 'Ǒ', 'O\\': 'Ǒ',
  
  // Vietnamese diacritical characters
  // a patterns
  'aw': 'ă', 'a8': 'ă',
  'AW': 'Ă', 'Aw': 'Ă', 'aW': 'Ă', 'A8': 'Ă',
  'aa': 'â', 'a6': 'â',
  'AA': 'Â', 'Aa': 'Â', 'aA': 'Â', 'A6': 'Â',
  
  // d patterns
  'dd': 'đ', 'd9': 'đ',
  'DD': 'Đ', 'Dd': 'Đ', 'dD': 'Đ', 'D9': 'Đ',
  
  // e patterns (additional)
  'ee': 'ê', 'e6': 'ê',
  'EE': 'Ê', 'Ee': 'Ê', 'eE': 'Ê', 'E6': 'Ê',
  
  // o patterns (additional)
  'oo': 'ô', 'o6': 'ô',
  'OO': 'Ô', 'Oo': 'Ô', 'oO': 'Ô', 'O6': 'Ô',
  'ow': 'ơ', 'o7': 'ơ',
  'OW': 'Ơ', 'Ow': 'Ơ', 'oW': 'Ơ', 'O7': 'Ơ',
  
  // u patterns (additional)
  'uw': 'ư', 'u7': 'ư',
  'UW': 'Ư', 'Uw': 'Ư', 'uW': 'Ư', 'U7': 'Ư'
};

// Cancellation patterns (same second character repeated)
const cancellationPatterns = {
  'e66': 'e6', 'E66': 'E6',
  'u88': 'u8', 'U88': 'U8',
  'c66': 'c6', 'C66': 'C6',
  'i88': 'i8', 'I88': 'I8',
  'n44': 'n4', 'N44': 'N4',
  'o88': 'o8', 'O88': 'O8',
  'uuu': 'uu', 'UUU': 'UU', 'Uuu': 'Uu',
  'ccc': 'cc', 'CCC': 'CC', 'Ccc': 'Cc',
  'eww': 'ew', 'EWW': 'EW', 'Eww': 'Ew',
  'iww': 'iw', 'IWW': 'IW', 'Iww': 'Iw',
  'nxx': 'nx', 'NXX': 'NX', 'Nxx': 'Nx',
  'n\\\\': 'n\\', 'N\\\\': 'N\\',
  'e\\\\': 'e\\', 'E\\\\': 'E\\',
  'u\\\\': 'u\\', 'U\\\\': 'U\\',
  'c\\\\': 'c\\', 'C\\\\': 'C\\',
  'i\\\\': 'i\\', 'I\\\\': 'I\\',
  'o\\\\': 'o\\', 'O\\\\': 'O\\',
  
  // Vietnamese character cancellations
  'a88': 'a8', 'A88': 'A8',
  'a66': 'a6', 'A66': 'A6',
  'aww': 'aw', 'AWW': 'AW', 'Aww': 'Aw',
  'aaa': 'aa', 'AAA': 'AA', 'Aaa': 'Aa',
  'd99': 'd9', 'D99': 'D9',
  'ddd': 'dd', 'DDD': 'DD', 'Ddd': 'Dd',
  'eee': 'ee', 'EEE': 'EE', 'Eee': 'Ee',
  'ooo': 'oo', 'OOO': 'OO', 'Ooo': 'Oo',
  'o66': 'o6', 'O66': 'O6',
  'o77': 'o7', 'O77': 'O7',
  'oww': 'ow', 'OWW': 'OW', 'Oww': 'Ow',
  'u77': 'u7', 'U77': 'U7',
  'uww': 'uw', 'UWW': 'UW', 'Uww': 'Uw'
};

function handleAutoReplace(event) {
  const textarea = event.target;
  const cursorPos = textarea.selectionStart;
  const text = textarea.value;
  
  // Check for cancellation patterns first (3 characters)
  if (cursorPos >= 3) {
    const last3 = text.substring(cursorPos - 3, cursorPos);
    if (cancellationPatterns[last3]) {
      const newText = text.substring(0, cursorPos - 3) + cancellationPatterns[last3] + text.substring(cursorPos);
      textarea.value = newText;
      textarea.setSelectionRange(cursorPos - 1, cursorPos - 1);
      autoGrow(textarea);
      return;
    }
  }
  
  // Check for replacement patterns (2 characters)
  if (cursorPos >= 2) {
    const last2 = text.substring(cursorPos - 2, cursorPos);
    if (replacements[last2]) {
      const newText = text.substring(0, cursorPos - 2) + replacements[last2] + text.substring(cursorPos);
      textarea.value = newText;
      textarea.setSelectionRange(cursorPos - 1, cursorPos - 1);
      autoGrow(textarea);
      return;
    }
  }
}

