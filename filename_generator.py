import hashlib
from datetime import datetime

def generate_filename(user_id: str, text: str, use_hash: bool =True):
    if use_hash:
        return f"tts_{hashlib.md5(user_id.encode()).hexdigest()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hashlib.md5(text.encode()).hexdigest()}.mp3"
    else:
        return f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"