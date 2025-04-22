from flask import Flask, request, jsonify
from tts.simple_gtts import SimpleGTTS

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

@app.route('/generate-speech', methods=['POST'])
def generate_speech():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # Required fields
    text = data.get('text')
    user_id = data.get('user_id')

    if not text or not user_id:
        return jsonify({"error": "Missing required parameters: 'text' and 'user_id'"}), 400

    # Optional fields
    filename = data.get('filename', 'default.mp3')
    output_dir = data.get('output_dir', 'output')
    detect_lang = data.get('detect_lang', False)

    try:
        tts = SimpleGTTS()
        output_path = tts.text_to_speech(
            raw_text=text,
            user=str(user_id),
            filename=filename,
            output_dir=output_dir,
            is_detect_lang=detect_lang
        )

        return jsonify({
            "message": "Speech generated successfully!",
            "file_path": output_path
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
