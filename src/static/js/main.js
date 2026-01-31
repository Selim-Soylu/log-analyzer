let currentEventSource = null;

function getSelectedFile() {
    return document.getElementById('fileSelect').value;
}

async function runStaticAnalysis() {
    const filename = getSelectedFile();
    const resultsDiv = document.getElementById('staticResults');
    resultsDiv.innerHTML = '<p class="info-text">Analiz ediliyor...</p>';

    const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filename: filename})
    });
    const data = await response.json();

    resultsDiv.innerHTML = '';
    if (data.length === 0) resultsDiv.innerHTML = '<p>Tehdit bulunamadı.</p>';
    
    data.forEach(log => {
        const div = document.createElement('div');
        div.className = `log-entry ${log.seviye}`;
        div.innerHTML = `<strong>[${log.seviye.toUpperCase()}] ${log.kural}</strong><br>${log.mesaj}`;
        resultsDiv.appendChild(div);
    });
}

function startStream() {
    const filename = getSelectedFile();
    const liveDiv = document.getElementById('liveStream');
    document.getElementById('activeStreamFile').innerText = filename;

    if (currentEventSource) currentEventSource.close();

    liveDiv.innerHTML = ''; 

    currentEventSource = new EventSource(`/api/stream/${filename}`);

    currentEventSource.onmessage = function(event) {
        if (event.data.startsWith("---")) {
             liveDiv.innerHTML += `<div style="color:cyan">${event.data}</div>`;
             return;
        }
        
        try {
            const log = JSON.parse(event.data);
            const div = document.createElement('div');
            div.className = 'live-entry';
            let color = 'white';
            if(log.seviye === 'high') color = 'red';
            else if(log.seviye === 'medium') color = 'orange';

            div.innerHTML = `<span style="color:${color}">[${log.seviye.toUpperCase()}] ${log.kural}</span> -> ${log.mesaj}`;
            liveDiv.appendChild(div);
            liveDiv.scrollTop = liveDiv.scrollHeight;
        } catch (e) {
             console.error("JSON hatası:", event.data);
        }
    };

    currentEventSource.onerror = function() {
        liveDiv.innerHTML += '<div style="color:red;">Yayın bağlantısı kesildi.</div>';
        currentEventSource.close();
    };
}