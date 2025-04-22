from tts.simple_gtts import SimpleGTTS

def main():
    dirty_text = """
    <h1>Halo semua!</h1>
    Ini adalah **contoh** teks <i>berantakan</i> dengan tag HTML, *markdown*, dan simbol seperti &lt;, &num; dan &amp;.
    """

    tts = SimpleGTTS()

    # Save to a custom folder and custom filename
    tts.text_to_speech(
        raw_text=dirty_text,
        filename="hasil_suara_2.mp3",
        output_dir="audio_output",
        is_play_audio=False
    )

if __name__ == "__main__":
    main()
