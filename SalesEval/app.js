import { projectData, personas } from './data.js';

let currentLang = 'ka';
let activePersona = null;
let chatHistory = [];
let isGrading = false;

const translations = {
    ka: {
        "setup-title": "აგენტების ტრენინგი",
        "setup-desc": "აირჩიეთ პერსონა სიმულაციის დასაწყებად.",
        "end-btn": "დასრულება და შეფასება",
        "results-title": "შეფასების რეპორტი",
        "metric-accuracy": "ინფორმაციის სიზუსტე",
        "metric-manner": "საუბრის მანერა და ტონი",
        "metric-soft": "კომუნიკაციის სტილი",
        "restart-btn": "ახალი სესია",
        "voice-listening": "გისმენთ...",
        "score-labels": ["გაუმჯობესება საჭიროა", "დამწყები", "კარგი", "პროფესიონალი", "ექსპერტი"],
        "placeholder": "ჩაწერეთ ან ისაუბრეთ...",
        "feedback-good-accuracy": "✅ პროექტის დეტალები (ROI, ფასები) ზუსტად არის გადმოცემული.",
        "feedback-bad-accuracy": "❌ პროექტის ფაქტობრივი მონაცემები არაზუსტია ან აკლია.",
        "feedback-good-manner": "✅ საუბრის ტემპი და ტონი დაცულია. საუბრობდით თავდაჯერებულად.",
        "feedback-bad-manner": "❌ საუბრის ტემპი ძალიან სწრაფია ან ბევრ 'პარაზიტ' სიტყვას იყენებთ (ანუ, ესე იგი).",
        "feedback-good-objection": "✅ წინააღმდეგობებს (ფასი, კლიმატი) კარგად ართმევთ თავს.",
        "feedback-bad-objection": "❌ მეტი აქცენტია საჭირო Escrow გარანტიებზე და კლიმატის უპირატესობაზე.",
        "feedback-cta": "💡 გახსოვდეთ: ყოველთვის მიუთითეთ სეილს პორტალზე ან შესთავაზეთ ზარი."
    },
    en: {
        "setup-title": "Agent Training",
        "setup-desc": "Select a persona to start the simulation.",
        "end-btn": "End & Grade",
        "results-title": "Evaluation Report",
        "metric-accuracy": "Information Accuracy",
        "metric-manner": "Voice Manner & Tone",
        "metric-soft": "Soft Skills",
        "restart-btn": "New Session",
        "voice-listening": "Listening...",
        "score-labels": ["Needs Improvement", "Beginner", "Good", "Professional", "Expert"],
        "placeholder": "Type or speak...",
        "feedback-good-accuracy": "✅ Project details (ROI, prices) are accurately conveyed.",
        "feedback-bad-accuracy": "❌ Project factual data is inaccurate or missing.",
        "feedback-good-manner": "✅ Speaking pace and tone are well-maintained. You sounded confident.",
        "feedback-bad-manner": "❌ Speaking pace is too fast or you use too many filler words (um, ah).",
        "feedback-cta": "💡 Reminder: Always mention the Sales Portal or offer a call."
    }
};

// UI Elements
const ui = {
    langToggle: document.getElementById('lang-toggle'),
    setupScreen: document.getElementById('setup-screen'),
    chatScreen: document.getElementById('chat-screen'),
    resultsScreen: document.getElementById('results-screen'),
    personaList: document.getElementById('persona-list'),
    chatMessages: document.getElementById('chat-messages'),
    chatInput: document.getElementById('chat-input'),
    sendBtn: document.getElementById('send-btn'),
    endBtn: document.getElementById('end-session'),
    voiceBtn: document.getElementById('voice-btn'),
    voiceStatus: document.getElementById('voice-status'),
    restartBtn: document.getElementById('restart-btn'),
    activePersonaName: document.getElementById('active-persona-name'),
    activePersonaAvatar: document.getElementById('active-persona-avatar'),
    typingIndicator: document.getElementById('typing-indicator'),
    finalScore: document.getElementById('final-score'),
    scoreText: document.getElementById('score-text'),
    feedbackArea: document.getElementById('feedback-area'),
    barAccuracy: document.getElementById('bar-accuracy'),
    barManner: document.getElementById('bar-objection'), 
    barSoft: document.getElementById('bar-soft')
};

let recognition = null;
let isRecording = false;
let recordStartTime = 0;
let fillerCount = 0;

// Initialize
function init() {
    renderPersonas();
    updateLanguageUI();
    initSpeechRecognition();
    
    ui.langToggle.addEventListener('click', toggleLanguage);
    ui.sendBtn.addEventListener('click', handleSend);
    ui.voiceBtn.addEventListener('click', toggleRecording);
    ui.endBtn.addEventListener('click', showResults);
    ui.restartBtn.addEventListener('click', resetApp);
    ui.chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });
}

function toggleLanguage() {
    currentLang = currentLang === 'ka' ? 'en' : 'ka';
    document.body.className = currentLang === 'ka' ? 'ka dark-theme' : 'dark-theme';
    updateLanguageUI();
    renderPersonas();
}

function updateLanguageUI() {
    const t = translations[currentLang];
    if (!t) return;
    
    document.querySelectorAll('[data-key]').forEach(el => {
        const key = el.getAttribute('data-key');
        if (t[key]) el.textContent = t[key];
    });
    ui.chatInput.placeholder = t['placeholder'] || '';
}

function renderPersonas() {
    ui.personaList.innerHTML = '';
    personas.forEach(p => {
        const name = p.name[currentLang] || p.name['en'] || 'Persona';
        const desc = p.description[currentLang] || p.description['en'] || '';
        
        const card = document.createElement('div');
        card.className = 'persona-card';
        card.innerHTML = `
            <div class="persona-avatar">${name[0]}</div>
            <h3>${name}</h3>
            <p>${desc}</p>
        `;
        card.onclick = () => startSession(p);
        ui.personaList.appendChild(card);
    });
}

function startSession(persona) {
    activePersona = persona;
    chatHistory = [];
    ui.setupScreen.classList.add('hidden');
    ui.chatScreen.classList.remove('hidden');
    
    const name = persona.name[currentLang] || persona.name['en'];
    ui.activePersonaName.textContent = name;
    ui.activePersonaAvatar.textContent = name[0];
    ui.chatMessages.innerHTML = '';
    
    const initialMsg = persona.initialMessage[currentLang] || persona.initialMessage['en'];
    addMessage('lead', initialMsg);
}

function addMessage(type, text) {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.textContent = text;
    ui.chatMessages.appendChild(msg);
    
    // Smooth scroll to bottom
    setTimeout(() => {
        ui.chatMessages.scrollTo({
            top: ui.chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }, 50);
    
    chatHistory.push({ type, text });
}

async function handleSend() {
    const text = ui.chatInput.value.trim();
    if (!text || isGrading) return;
    
    addMessage('agent', text);
    ui.chatInput.value = '';
    
    // Show Typing Indicator
    setTimeout(async () => {
        ui.typingIndicator.classList.remove('hidden');
        ui.chatMessages.scrollTop = ui.chatMessages.scrollHeight;
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    messages: chatHistory.map(m => ({
                        role: m.type === 'lead' ? 'assistant' : 'user',
                        content: m.text
                    })),
                    persona: activePersona.id,
                    lang: currentLang
                })
            });
            
            const data = await response.json();
            ui.typingIndicator.classList.add('hidden');
            
            if (data.message) {
                addMessage('lead', data.message);
            } else {
                throw new Error('Empty response');
            }
        } catch (error) {
            console.error('AI Error:', error);
            ui.typingIndicator.classList.add('hidden');
            addMessage('lead', currentLang === 'ka' ? 'ბოდიში, კავშირის პრობლემა მაქვს...' : 'Sorry, I am having connection issues...');
        }
    }, 500);
}

async function showResults() {
    isGrading = true;
    ui.chatScreen.classList.add('hidden');
    ui.resultsScreen.classList.remove('hidden');
    
    // Show loading state for evaluation
    ui.finalScore.textContent = '...';
    ui.scoreText.textContent = currentLang === 'ka' ? 'მიმდინარეობს ანალიზი...' : 'Analyzing performance...';
    
    try {
        const response = await fetch('/api/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                history: chatHistory,
                lang: currentLang
            })
        });
        
        const scores = await response.json();
        
        ui.finalScore.textContent = scores.total;
        ui.barAccuracy.style.width = scores.accuracy + '%';
        ui.barManner.style.width = scores.manner + '%';
        ui.barSoft.style.width = scores.soft + '%';
        
        const labels = translations[currentLang]['score-labels'];
        const labelIndex = Math.min(Math.floor(scores.total / 2), labels.length - 1);
        ui.scoreText.textContent = labels[labelIndex];

        renderFeedback(scores.feedback);
        
        // Log to history
        logSession(scores);
        
    } catch (error) {
        console.error('Evaluation Error:', error);
        ui.scoreText.textContent = 'Error in analysis';
    } finally {
        isGrading = false;
    }
}

function renderFeedback(feedback) {
    ui.feedbackArea.innerHTML = '';
    feedback.forEach(text => {
        const div = document.createElement('div');
        div.className = 'feedback-item';
        div.textContent = text;
        ui.feedbackArea.appendChild(div);
    });
}

function logSession(scores) {
    try {
        fetch('/api/log', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                timestamp: new Date().toLocaleString(),
                persona: activePersona.name[currentLang],
                score: scores.total,
                accuracy: scores.accuracy,
                manner: scores.manner,
                soft: scores.soft,
                transcript: chatHistory.map(m => `${m.type.toUpperCase()}: ${m.text}`).join('\n')
            })
        });
    } catch (e) {
        console.warn('Logging failed:', e);
    }
}

function initSpeechRecognition() {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (window.SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.interimResults = true;
        recognition.continuous = true;

        recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(result => result[0])
                .map(result => result.transcript)
                .join('');
            ui.chatInput.value = transcript;
            
            // Detect fillers
            const fillers = ["ანუ", "ესე იგი", "um", "ah", "like", "so"];
            fillers.forEach(f => {
                if (transcript.toLowerCase().endsWith(f)) {
                    fillerCount++;
                }
            });
        };

        recognition.onend = () => {
            if (isRecording) recognition.start();
        };
    } else {
        ui.voiceBtn.style.display = 'none';
        console.warn('Speech recognition not supported');
    }
}

function toggleRecording() {
    if (!isRecording) {
        startRecording();
    } else {
        stopRecording();
    }
}

function startRecording() {
    isRecording = true;
    recordStartTime = Date.now();
    ui.voiceBtn.classList.add('recording');
    ui.voiceStatus.classList.remove('hidden');
    recognition.lang = currentLang === 'ka' ? 'ka-GE' : 'en-US';
    recognition.start();
}

function stopRecording() {
    isRecording = false;
    ui.voiceBtn.classList.remove('recording');
    ui.voiceStatus.classList.add('hidden');
    recognition.stop();
}

function resetApp() {
    ui.resultsScreen.classList.add('hidden');
    ui.setupScreen.classList.remove('hidden');
    activePersona = null;
    chatHistory = [];
    fillerCount = 0;
}

init();
