import re
import html
from gtts import gTTS
import os
import hashlib
from datetime import datetime
from langdetect import detect

class SimpleGTTS:
    def __init__(self, lang='id'):
        """
        Initialize the SimpleGTTS object.
        """
        self.lang = lang

    def clean_text(self, raw_text):
        """
        Clean raw text from HTML, Markdown, and HTML entities.

        Steps:
        Remove HTML tags (e.g., <p>, <div>, etc.).
        Remove common Markdown formatting characters (* _ ~ `).
        Convert HTML entities to their corresponding characters (e.g., &amp; -> &).
        Normalize whitespace: replace multiple spaces with a single space, and trim leading/trailing spaces.
        """
        # Remove HTML tags using a regex pattern that matches anything between < and >
        text = re.sub(r'<[^>]+>', '', raw_text)

        # Remove Markdown formatting symbols like *, _, ~, and `
        text = re.sub(r'[*_~`]', '', text)

        # Convert HTML entities (e.g., &nbsp;, &amp;) to their actual characters
        text = html.unescape(text)

        # Replace multiple whitespace characters with a single space, then strip leading/trailing spaces
        text = re.sub(r'\s+', ' ', text).strip()

        return text
    
    def generate_filename(self, user_id: str, text: str, use_hash: bool =True):
        if use_hash:
            return f"tts_{hashlib.md5(user_id.encode()).hexdigest()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(text.encode()).hexdigest()}.mp3"
        else:
            return f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
        
    def detect_language(self, text):
        """
        Detect the language of the input text using langdetect.
        """
        try:
            lang = detect(text)
            return lang
        except Exception as e:
            print(f"Error detecting language: {e}")
            return None

    def text_to_speech(self, raw_text, user, filename="default.mp3", output_dir="output", is_detect_lang=False):
        """
        Convert cleaned text to speech and save it to a dynamically specified path.
        
        :param raw_text: The input text (may contain HTML/markdown/etc.)
        :param filename: The output file name (e.g., "voice.mp3")
        :param output_dir: The directory to save the output file
        :param is_play_audio: Whether to play the file after generation
        """
        cleaned = self.clean_text(raw_text)

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename if filename != "default.mp3" else self.generate_filename(user, cleaned))

        # Generate and save TTS audio
        tts = gTTS(text=cleaned, lang=self.lang if not is_detect_lang else self.detect_language(cleaned))
        tts.save(output_path)

        # Optionally play
        # if is_play_audio:
        #     self._play_audio(output_path)

        return output_path


    def _play_audio(self, file_path):
        """
        Play an audio file depending on the OS.
        """
        if os.name == 'nt':
            os.system(f'start {file_path}')
        elif os.name == 'posix':
            os.system(f'afplay {file_path}') or os.system(f'mpg123 {file_path}')
