import re
import html
from gtts import gTTS
import os

def clean_text(raw_text):
    """
    Clean text from HTML tags, Markdown symbols, and HTML entities.
    """
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', raw_text)
    
    # Remove Markdown symbols like **bold**, *italic*, `code`, etc.
    text = re.sub(r'[*_~`]', '', text)
    
    # Decode HTML entities (e.g., &amp; -> &)
    text = html.unescape(text)
    
    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Example dirty text in Indonesian
dirty_text = """
<h1>Halo semua!</h1>
Ini adalah **contoh** teks <i>berantakan</i> dengan tag HTML, *markdown*, dan simbol seperti &lt;, &num; dan &amp;.
"""

# Clean the text
cleaned_text = clean_text(dirty_text)

print("Cleaned Text:", cleaned_text)

# Convert to Indonesian speech
tts = gTTS(text=cleaned_text, lang='id')
tts.save("clean_output_id.mp3")

# Play the result
os.system("start clean_output_id.mp3")  # For Windows
