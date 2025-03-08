from flask import Flask, render_template, request, jsonify
from gtts import gTTS
import os
import tempfile
import base64
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/speak', methods=['POST'])
def speak():
    try:
        data = request.get_json()
        text = data.get('text', '')
        speed = float(data.get('speed', 1.0))  # Note: gTTS doesn't support speed adjustment
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400

        logger.info(f"Processing text: {text[:50]}...")

        # Create temporary file for audio
        temp_path = os.path.join(tempfile.gettempdir(), 'speech.mp3')
        logger.info(f"Created temp file: {temp_path}")
            
        # Generate speech
        tts = gTTS(text=text, lang='en')
        tts.save(temp_path)
        
        # Check if file was created and has content
        if not os.path.exists(temp_path):
            raise Exception("Audio file was not created")
            
        file_size = os.path.getsize(temp_path)
        logger.info(f"Audio file size: {file_size} bytes")
        
        if file_size == 0:
            raise Exception("Audio file is empty")
            
        # Read the file and return it as base64
        with open(temp_path, 'rb') as fp:
            audio_data = base64.b64encode(fp.read()).decode('utf-8')
            
        # Clean up
        os.unlink(temp_path)
        logger.info("Audio file processed and cleaned up successfully")
        
        return jsonify({
            'success': True,
            'audio': audio_data
        })
        
    except Exception as e:
        logger.error(f"Error in speak route: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 