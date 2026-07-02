const projectData = {
    ka: {
        name: "Green Canyon",
        location: "წალკა, საქართველო (1500მ სიმაღლეზე)",
        roi: "8-12% წლიური",
        capitalAppreciation: "20-30% მშენებლობის დასრულებამდე",
        prices: {
            studio: "$59,500-დან",
            oneBed: "$85,000-დან",
            cottages: "$150,000-დან $440,000-მდე"
        },
        paymentTerms: {
            downpayment: "15-30%",
            installments: "36 თვიანი 0% განვადება",
            escrow: "საერთაშორისო Escrow ანგარიშები (ბანკის გარანტია)"
        },
        timeline: {
            start: "2026 წლის ზაფხული",
            completion: "2030 წლის გაზაფხული (36 თვე)"
        },
        features: ["LEED/Green Globe სერთიფიკატი", "Radisson Standard MEP", "Smart Home", "სპა, რესტორანი, ზიპ-ლაინი"],
        objections: {
            price: "თქვენ ყიდულობთ 5-ვარსკვლავიან ეკოსისტემას და ტერნქეი რემონტს (Bosch/Grohe).",
            climate: "გრილი ზაფხული (20-22°C) - საუკეთესო თავშესაფარი სიცხისგან.",
            trust: "Escrow ანგარიში - დეველოპერი ფულს იღებს მხოლოდ ეტაპების ჩაბარების შემდეგ."
        }
    },
    en: {
        name: "Green Canyon",
        location: "Tsalka, Georgia (1500m altitude)",
        roi: "8-12% Annual",
        capitalAppreciation: "20-30% before completion",
        prices: {
            studio: "From $59,500",
            oneBed: "From $85,000",
            cottages: "From $150,000 to $440,000"
        },
        paymentTerms: {
            downpayment: "15-30%",
            installments: "36-month 0% installments",
            escrow: "International Escrow accounts (Bank guarantee)"
        },
        timeline: {
            start: "Summer 2026",
            completion: "Spring 2030 (36 months)"
        },
        features: ["LEED/Green Globe Certification", "Radisson Standard MEP", "Smart Home", "Spa, Restaurant, Zip-line"],
        objections: {
            price: "You are purchasing a 5-star ecosystem with turnkey renovation (Bosch/Grohe).",
            climate: "Cool summer (20-22°C) - the best escape from heat.",
            trust: "Escrow account - direct developer payment only after stage completion."
        }
    }
};

// Build Timestamp: 2026-04-21 11:20
const personas = [
    {
        id: "investor",
        name: { ka: "ბატონი ხანი", en: "Mr. Khan", ge: "ბატონი ხანი" },
        description: { ka: "ინვესტორი დუბაიდან, აინტერესებს ROI და უსაფრთხოება.", en: "Investor from Dubai, interested in ROI and safety.", ge: "ინვესტორი დუბაიდან" },
        initialMessage: { ka: "გამარჯობა, მაინტერესებს თქვენი პროექტი. რა გარანტიები მაქვს და რა იქნება ჩემი წლიური მოგება?", en: "Hello, I'm interested in your project. What guarantees do I have and what will be my annual return?", ge: "გამარჯობა, მაინტერესებს თქვენი პროექტი." },
        traits: ["skeptical", "logical", "safety-first"]
    },
    {
        id: "wellness",
        name: { ka: "თამარი", en: "Tamar", ge: "თამარი" },
        description: { ka: "ადგილობრივი მაცხოვრებელი, ეძებს აგარაკს ოჯახისთვის.", en: "Local resident, looking for a cottage for her family.", ge: "ადგილობრივი მაცხოვრებელი" },
        initialMessage: { ka: "გამარჯობა, წალკა ძალიან ცივი ხომ არ არის? და რითია თქვენი კოტეჯები გამორჩეული?", en: "Hello, isn't Tsalka too cold? And what makes your cottages special?", ge: "გამარჯობა, წალკა ძალიან ცივი ხომ არ არის?" },
        traits: ["lifestyle-oriented", "nature-lover"]
    }
];

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
        const name = p.name[currentLang] || p.name['ge'] || p.name['en'] || 'Persona';
        const desc = p.description[currentLang] || p.description['ge'] || p.description['en'] || '';
        
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
    
    const name = persona.name[currentLang] || persona.name['ge'] || persona.name['en'];
    ui.activePersonaName.textContent = name;
    ui.activePersonaAvatar.textContent = name[0];
    ui.chatMessages.innerHTML = '';
    
    const initialMsg = persona.initialMessage[currentLang] || persona.initialMessage['ge'] || persona.initialMessage['en'];
    addMessage('lead', initialMsg);
}

function addMessage(type, text, saveToHistory = true) {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.textContent = text;
    ui.chatMessages.appendChild(msg);
    
    // Improved scrolling logic
    requestAnimationFrame(() => {
        ui.chatMessages.scrollTop = ui.chatMessages.scrollHeight;
        // Backup for smooth feel
        setTimeout(() => {
            ui.chatMessages.scrollTop = ui.chatMessages.scrollHeight;
        }, 100);
    });
    
    if (saveToHistory) {
        chatHistory.push({ type, text });
    }
}

async function handleSend() {
    const text = ui.chatInput.value.trim();
    if (!text || isGrading) return;
    
    addMessage('agent', text);
    ui.chatInput.value = '';
    
    // Reset Speech Recognition buffer if active to prevent duplication
    if (isRecording && recognition) {
        recognition.stop();
        // It will auto-restart in onend if isRecording is true, 
        // which clears the internal results buffer
    }
    
    ui.typingIndicator.classList.remove('hidden');
    ui.chatMessages.scrollTop = ui.chatMessages.scrollHeight;
    
    try {
        const response = await fetch(`/.netlify/functions/chat?t=${Date.now()}`, {
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
        console.log('Chat Version:', data.version || 'v5.0-Legacy');
        
        if (!response.ok) {
            throw new Error(data.error || 'API Sync issue');
        }
        
        ui.typingIndicator.classList.add('hidden');
        if (data.message) addMessage('lead', data.message);
    } catch (error) {
        console.error('AI Offline:', error);
        ui.typingIndicator.classList.add('hidden');
        addMessage('lead', currentLang === 'ka' ? `ბოდიში, კავშირის პრობლემა მაქვს (${error.message}).` : `Sorry, connection issue (${error.message}).`, false);
    }
}

async function showResults() {
    isGrading = true;
    ui.chatScreen.classList.add('hidden');
    ui.resultsScreen.classList.remove('hidden');
    ui.finalScore.textContent = '...';
    
    try {
        const response = await fetch(`/.netlify/functions/evaluate?t=${Date.now()}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                history: chatHistory, 
                persona: activePersona.id,
                lang: currentLang 
            })
        });
        
        const scores = await response.json();
        console.log('Eval Version:', scores._version || scores.version || 'v5.0-Legacy');

        if (!response.ok) {
            throw new Error(scores.error || 'Evaluation Failed');
        }

        ui.finalScore.textContent = scores.score || 0;
        ui.barAccuracy.style.width = (scores.accuracy || 0) + '%';
        ui.barManner.style.width = (scores.objection || 0) + '%'; // objection -> manner bar
        ui.barSoft.style.width = (scores.softSkills || 0) + '%'; // softSkills -> soft bar
        
        const labels = translations[currentLang]['score-labels'];
        const total = scores.score || 0;
        ui.scoreText.textContent = labels[Math.min(Math.floor(total / 2), labels.length - 1)];
        renderFeedback(scores.feedback || []);
        logSession(scores);
    } catch (error) {
        console.error('Eval Error:', error);
        ui.finalScore.textContent = '!';
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
    fetch(`/.netlify/functions/log?t=${Date.now()}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            timestamp: new Date().toLocaleString(),
            persona: activePersona.name[currentLang],
            score: scores.score,
            accuracy: scores.accuracy,
            manner: scores.objection,
            soft: scores.softSkills,
            transcript: chatHistory.map(m => `${m.type.toUpperCase()}: ${m.text}`).join('\n')
        })
    }).catch(e => console.warn('Log error'));
}

function initSpeechRecognition() {
    window.SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (window.SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.interimResults = true;
        recognition.continuous = true;
        recognition.onresult = (e) => {
            ui.chatInput.value = Array.from(e.results).map(r => r[0].transcript).join('');
        };
        recognition.onend = () => { if (isRecording) recognition.start(); };
    } else {
        ui.voiceBtn.style.display = 'none';
    }
}

function toggleRecording() {
    if (!isRecording) {
        isRecording = true;
        ui.voiceBtn.classList.add('recording');
        ui.voiceStatus.classList.remove('hidden');
        recognition.lang = currentLang === 'ka' ? 'ka-GE' : 'en-US';
        recognition.start();
    } else {
        isRecording = false;
        ui.voiceBtn.classList.remove('recording');
        ui.voiceStatus.classList.add('hidden');
        recognition.stop();
    }
}

function resetApp() {
    ui.resultsScreen.classList.add('hidden');
    ui.setupScreen.classList.remove('hidden');
    activePersona = null;
    chatHistory = [];
}

init();
