from gtts import gTTS

def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    tts.save('audio.mp3')
