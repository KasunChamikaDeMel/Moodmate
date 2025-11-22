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

// Add new animations for pet activities
const activityAnimations = {
    feed: 'assets/happy-1.json', // Placeholder, ideally specific feed animation
    play: 'assets/happy-2.json', // Placeholder
    clean: 'assets/idle-3.json', // Placeholder
    train: 'assets/idle-4.json'  // Placeholder
};

const petTypeAnimations = {
    cat: {
        idle: 'assets/idle-1.json',
        happy: 'assets/happy-1.json',
        sleepy: 'assets/sleep-1.json',
        angry: 'assets/idle-2.json',
        love: 'assets/love-1.json'
    },
    dog: {
        idle: 'assets/idle-1.json', // Placeholder for dog idle
        happy: 'assets/happy-1.json',
        sleepy: 'assets/sleep-1.json',
        angry: 'assets/idle-2.json',
        love: 'assets/love-1.json'
    },
    bunny: {
        idle: 'assets/idle-1.json', // Placeholder for bunny idle
        happy: 'assets/happy-1.json',
        sleepy: 'assets/sleep-1.json',
        angry: 'assets/idle-2.json',
        love: 'assets/love-1.json'
    }
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


// Expose global functions for PySide6 to call
window.setPetType = function(type) {
    currentPetType = type;
    // Load default idle animation for the new pet type
    const anim = petTypeAnimations[currentPetType]?.idle || allAnimations[0];
    playSpecificAnimation(anim);
    console.log(`Pet type set to: ${type}`);
};

window.setPetMood = function(mood) {
    currentPetMood = mood;
    let animPath = uniqueAnimations[mood];
    if (!animPath && petTypeAnimations[currentPetType] && petTypeAnimations[currentPetType][mood]) {
        animPath = petTypeAnimations[currentPetType][mood];
    }
    playSpecificAnimation(animPath || allAnimations[0]);
    console.log(`Pet mood set to: ${mood}`);
};

window.playAnimation = function(action) {
    const animPath = activityAnimations[action];
    if (animPath) {
        playSpecificAnimation(animPath);
        console.log(`Playing animation for action: ${action}`);
        // After playing the action animation, revert to current mood animation or idle
        setTimeout(() => {
            window.setPetMood(currentPetMood || 'idle'); // Revert to mood or idle
        }, 2000); // Assume animation takes 2 seconds
    } else {
        console.warn(`No animation defined for action: ${action}`);
    }
};

// Initial state
let currentPetType = 'cat';
let currentPetMood = 'idle';

petAnim.addEventListener('mousedown', (e) => {
    if (e.button === 0) {
        isInteracting = true;
        if (idleLoopTimer) clearInterval(idleLoopTimer);

        playSpecificAnimation('assets/love-1.json'); 
        
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

        petAnim.style.cursor = "grabbing";
    }
});

window.addEventListener('mouseup', () => {
    petAnim.style.cursor = "grab";
});
window.addEventListener('contextmenu', (e) => { e.preventDefault(); });