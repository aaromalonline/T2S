document.addEventListener('DOMContentLoaded', function() {
    const textInput = document.getElementById('textInput');
    const speedRange = document.getElementById('speedRange');
    const speedValue = document.getElementById('speedValue');
    const speakButton = document.getElementById('speakButton');
    const status = document.getElementById('status');
    
    speedRange.addEventListener('input', function() {
        speedValue.textContent = `${this.value}x`;
    });
    
    speakButton.addEventListener('click', async function() {
        const text = textInput.value.trim();
        if (!text) {
            status.textContent = 'Please enter some text!';
            status.className = 'status error';
            return;
        }
        
        try {
            status.textContent = 'Speaking...';
            status.className = 'status speaking';
            speakButton.disabled = true;
            
            const response = await fetch('/speak', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    speed: parseFloat(speedRange.value)
                })
            });
            
            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            // Convert base64 to blob
            const audioData = atob(data.audio);
            const arrayBuffer = new ArrayBuffer(audioData.length);
            const uint8Array = new Uint8Array(arrayBuffer);
            for (let i = 0; i < audioData.length; i++) {
                uint8Array[i] = audioData.charCodeAt(i);
            }
            
            // Create blob and play audio
            const blob = new Blob([uint8Array], { type: 'audio/mp3' });
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            
            audio.onended = function() {
                status.textContent = 'Ready';
                status.className = 'status ready';
                speakButton.disabled = false;
                URL.revokeObjectURL(audioUrl);
            };
            
            audio.play();
            
        } catch (error) {
            status.textContent = `Error: ${error.message}`;
            status.className = 'status error';
            speakButton.disabled = false;
        }
    });
}); 