from gtts import gTTS
from pydub import AudioSegment
from reddit_text import find_aita

def generate_audio():
    tts = gTTS(text=find_aita(), lang='en')
    tts.save('audio.mp3')


def speed_up_audio(input_file, output_file, speed_factor=1.3):
    # Load the audio file
    audio = AudioSegment.from_file(input_file, format="mp3")
    
    # Speed up the audio
    sped_up_audio = audio.speedup(playback_speed=speed_factor)
    
    # Export the sped-up audio to a new file
    sped_up_audio.export(output_file, format="mp3")
