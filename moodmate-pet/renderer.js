const { ipcRenderer } = require('electron');
const petAnim = document.getElementById('pet-anim');
const bubble = document.getElementById('bubble');

let hideTimer = null;
let isInteracting = false;
let lastPlayedAnim = null;
let idleLoopTimer = null;
let messageSequenceTimer = null;

// --- 1. GIF DATABASE ---
const allAnimations = [
    'assets/idle-1.json', 'assets/idle-2.json',
    'assets/idle-3.json', 'assets/idle-4.json',
    'assets/idle-5.json', 'assets/idle-6.json',
    'assets/idle-7.json',
    'assets/happy-1.json', 'assets/sleep-1.json',
    'assets/chargeon.json', 'assets/wifion.json'
];

const uniqueAnimations = {
    stress: 'assets/sleep-1.json',
    angry: 'assets/idle-2.json',
    sleepy: 'assets/sleep-1.json',
    happy: 'assets/happy-1.json',
    love: 'assets/love-1.json',
    poweroff : 'assets/chargeoff.json',
    poweron : 'assets/chargeon.json',
    wifioff: 'assets/wifioff.json',
    wifion: 'assets/wifion.json'

};

// --- 2. FULL DATA SET ---
const emotionData = {
"stress": { 
        "icon": "😰", 
        "pet_says": ["You got this!", "Reset & Restart.", "Don't give up!"],
        "tips": [
            "Prioritize tasks. ✅", 
            "Take a deep breath. 🧘", 
            "Focus on one thing. 🎯"
        ] 
    },
    "angry": { 
        "icon": "😤", 
        "pet_says": ["Channel that energy!", "Stay focused.", "Don't lose control."], 
        "tips": [
            "Listen to Lofi music. 🎧", 
            "Count to 10. 🔟", 
            "Drink water. 💧"
        ] 
    },
    "sleepy": { 
        "icon": "🥱", 
        "pet_says": ["Wake up!", "Stay sharp!", "Eyes on screen!"], 
        "tips": [
            "Splash cold water. 💦", 
            "Stand up & stretch. 🙆", 
            "Turn on bright lights. 💡"
        ] 
    },
    "sleep": { 
        "icon": "🚫", 
        "pet_says": ["No sleeping yet!", "Keep grinding!", "Finish the goal!"], 
        "tips": [
            "Do 5 jumping jacks. 🏃", 
            "Walk for 2 mins. 🚶", 
            "Drink some coffee. ☕"
        ] 
    },
    "poweroff": { 
        "icon": "🔌", 
        "pet_says": ["Running on battery.", "Charger removed!", "Save power!"],
        "tips": [
            "Lower screen brightness. 🔅", 
            "Close unused apps. 📉", 
            "Plug in at 20%. 🔋"
        ]
    },
    "poweron": { 
        "icon": "⚡", 
        "pet_says": ["Unlimited Power!", "Energized!", "Charging now!"],
        "tips": [
            "Good for heavy tasks. 🚀", 
            "Increase brightness. 🔆", 
            "Unplug at 100%. ❤️"
        ]
    },
    "wifioff": { 
        "icon": "📡", 
        "pet_says": ["No connection...", "It's too quiet...", "Where is the Wi-Fi?"],
        "tips": [
            "Check your router. 📶", 
            "Restart Wi-Fi. 🔄", 
            "Clean your desktop. 📂"
        ] 
    },
    "wifion": { 
        "icon": "🌐", 
        "pet_says": ["Back online!", "Connected!", "Internet is back!"],
        "tips": [
            "Check your emails. 📧", 
            "Cloud sync active. ☁️", 
            "Update your apps. 📲"
        ] 
    }
};

// Start
playRandomFromAll();
resetIdleTimer();


// --- FUNCTIONS ---
function resetIdleTimer() {
    if (idleLoopTimer) clearInterval(idleLoopTimer);
    idleLoopTimer = setInterval(() => {
        if (!isInteracting) {
            playRandomFromAll();
            bubble.style.display = 'none';
        }
    }, 15000);
}

function playSpecificAnimation(animPath) {
    if(animPath) {
        petAnim.load(animPath);
        petAnim.setSpeed(1);
        lastPlayedAnim = animPath;
    }
}

function playRandomFromAll() {
    const availableAnims = allAnimations.filter(anim => anim !== lastPlayedAnim);
    let randomAnim = availableAnims.length > 0 
        ? availableAnims[Math.floor(Math.random() * availableAnims.length)] 
        : allAnimations[0];

    petAnim.load(randomAnim);
    petAnim.setSpeed(0.8);
    lastPlayedAnim = randomAnim;
    bubble.style.display = 'none';
}


// --- 3. BACKEND TRIGGER (Lassana UI Logic) ---
ipcRenderer.on('backend-trigger', (event, data) => {
    resetIdleTimer(); 
    if (hideTimer) clearTimeout(hideTimer);
    if (messageSequenceTimer) clearTimeout(messageSequenceTimer);
    
    isInteracting = false; 
    const emotion = data.emotion || 'happy';

    if (uniqueAnimations[emotion]) {
        playSpecificAnimation(uniqueAnimations[emotion]);
    } else {
        playSpecificAnimation('assets/happy-1.json');
    }

    const eData = emotionData[emotion];
    
    if (eData) {
        const randomSay = eData.pet_says[Math.floor(Math.random() * eData.pet_says.length)];
        const randomTip = eData.tips[Math.floor(Math.random() * eData.tips.length)];

        // 🛑 STEP 1: "Pet Says" (ලස්සන Icon එකත් එක්ක)
        bubble.innerHTML = `
            <div class="emoji-icon">${eData.icon}</div>
            <div style="font-weight:600; color:#2d3436;">${randomSay}</div>
        `;
        bubble.style.display = 'block';

        // 🛑 STEP 2: Tip එක (Badge එකක් එක්ක)
        messageSequenceTimer = setTimeout(() => {
            bubble.innerHTML = `
                <div class="tip-badge">💡 Quick Tip</div>
                <div style="font-weight:500;">${randomTip}</div>
            `;
        }, 4000); 

    } else {
        bubble.innerText = data.message || "Meow! 😺";
        bubble.style.display = 'block';
    }
});


// --- 4. USER INTERACTION ---
petAnim.addEventListener('mousedown', (e) => {
    if (e.button === 0) {
        ipcRenderer.send('stop-timer');
        isInteracting = true;
        if (idleLoopTimer) clearInterval(idleLoopTimer);

        playSpecificAnimation('assets/love-1.json'); 
        
        // Click මැසේජ් එක
        bubble.innerHTML = `
            <div class="emoji-icon">❤️</div>
            <div style="font-weight:bold; color:#e17055;">I Love You!</div>
        `;
        bubble.style.display = 'block';

        setTimeout(() => {
            isInteracting = false; 
            playRandomFromAll(); 
            resetIdleTimer(); 
        }, 2000);

        const offsetX = e.clientX;
        const offsetY = e.clientY;
        ipcRenderer.send('drag-start', { x: offsetX, y: offsetY });
        petAnim.style.cursor = "grabbing";
    }
});

window.addEventListener('mouseup', () => {
    ipcRenderer.send('drag-end');
    petAnim.style.cursor = "grab";
});
// Standard listeners...
petAnim.addEventListener('mouseenter', () => ipcRenderer.send('set-ignore-mouse', false));
petAnim.addEventListener('mouseleave', () => ipcRenderer.send('set-ignore-mouse', true));
window.addEventListener('contextmenu', (e) => { e.preventDefault(); ipcRenderer.send('show-context-menu'); });
ipcRenderer.on('apply-setting', (event, data) => { if (data.type === 'opacity') petAnim.style.opacity = data.value; });