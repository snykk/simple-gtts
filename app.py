import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from tts.simple_gtts import SimpleGTTS

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/generate-speech':
            # Get content length and read the data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse JSON data
            try:
                data = json.loads(post_data.decode())
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON format"}).encode())
                return

            # Check for required fields
            if 'text' not in data or 'user_id' not in data:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing required parameters: 'text' and 'user_id'"}).encode())
                return

            text = data['text']
            user_id = data['user_id']
            filename = data.get('filename', 'default.mp3')
            output_dir = data.get('output_dir', 'output')
            detect_lang = data.get('detect_lang', False)

            print(user_id)
            print(type(user_id))

            # Initialize SimpleGTTS
            tts = SimpleGTTS()

            try:
                output_path = tts.text_to_speech(
                    raw_text=text,
                    user=str(user_id),
                    filename=filename,
                    output_dir=output_dir,
                    is_detect_lang=detect_lang
                )

                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "message": "Speech generated successfully!",
                    "file_path": os.path.join(output_dir, output_path)
                }).encode())

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_GET(self):
        if self.path == '/health':
            # Health check endpoint
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "OK"}).encode())


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
