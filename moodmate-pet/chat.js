const btn = document.getElementById('btn');
const inp = document.getElementById('msg');
const box = document.getElementById('chat-box');

function send() {
    const txt = inp.value.trim();
    if(!txt) return;
    
    addMsg(txt, 'user');
    inp.value = ''; // Input එක හිස් කරන්න

    // DeepSeek / Gemini (Port 5001) එකට යවනවා
    fetch('http://127.0.0.1:5001/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: txt })
    })
    .then(r => r.json())
    .then(d => addMsg(d.reply, 'bot'))
    .catch(e => addMsg("Offline 😿", 'bot'));
}

function addMsg(t, c) {
    const d = document.createElement('div');
    d.className = `message ${c}`;
    d.innerText = t;
    box.appendChild(d);
    // මැසේජ් එකක් ආපු ගමන් යටටම Scroll කරන්න
    box.scrollTop = box.scrollHeight;
}

// Button Click
btn.onclick = send;

// ENTER KEY LOGIC (මේක තමයි ඔයා ඉල්ලපු කොටස)
inp.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Default Enter වැඩේ නවත්තලා
        send(); // Send Function එක කෝල් කරනවා
    }
});