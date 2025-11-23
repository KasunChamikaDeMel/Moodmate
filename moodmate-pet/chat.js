const btn = document.getElementById('btn');
const inp = document.getElementById('msg');
const box = document.getElementById('chat-box');

function send() {
    const txt = inp.value.trim();
    if(!txt) return;
    
    addMsg(txt, 'user');
    inp.value = ''; // Input be empty after sending

    //  Gemini (Port 5001) 
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
    // scroll to bottom when message added
    box.scrollTop = box.scrollHeight;
}

// Button Click
btn.onclick = send;

// ENTER KEY LOGIC
inp.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault(); // Default Enter behavior stopped
        send();
    }
});