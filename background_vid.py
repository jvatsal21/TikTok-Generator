import openai
import os
from pathlib import Path
from openai import OpenAI
from reddit_text import find_aita   

# Set the API key for OpenAI
openai.api_key = os.environ["OPENAI_API_KEY"]

# Path to save the speech file
speech_file_path = Path(__file__).parent / "output.mp3"

# Create speech from text
response = openai.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input=find_aita()
)

# Save the speech to a file
with open(speech_file_path, "wb") as audio_file:
    audio_file.write(response.content)

print(f"Audio file saved as {speech_file_path}")