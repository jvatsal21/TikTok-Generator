import os
from gtts import gTTS
from reddit_text import find_aita   

# Text you want to convert to speech
text_to_speak = find_aita()

# Create a gTTS object
tts = gTTS(text_to_speak, lang='en')

# Save the spoken text to an MP3 file
tts.save("output.mp3")

print("The speech has been saved as 'output.mp3'")