from pydub import AudioSegment
import subprocess
from moviepy.editor import AudioFileClip
import tempfile
import os

def generate_audio(text, sessionID, voice, is_title):
    """
    Generate an audio clip from the given text using the specified voice and TikTok session ID.

    Args:
        text (str): The text to be converted to audio.
        sessionID (str): The TikTok session ID for the text-to-speech conversion.
        voice (str): The voice to be used for the text-to-speech conversion.
        is_title (bool): Indicates whether the text is a title or not.

    Returns:
        AudioFileClip: The generated audio clip.
    """
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=True, suffix='.txt') as text_file:
        text_file.write(text)
        text_file.flush()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as audio_file:
        audio_file_path = audio_file.name


        # Create a list of command arguments for the text-to-speech conversion
        command = [
            'python3', 'src/tts.py',
            '-v', voice,
            '-f', text_file.name,
            '-n', audio_file_path, 
            '--session', sessionID
        ]
        
        # Run the text-to-speech conversion command
        subprocess.run(command, text=True, capture_output=True)
    
    if not os.path.exists(audio_file_path) or :
            raise IOError("Failed to generate audio file")

    audio_clip = AudioFileClip(audio_file_path)

    # If performing TTS on non-title text, cut audio sligtly at the end
    # This addresses a slight bug with audio concatenation
    if not is_title:
        duration = audio_clip.duration
        new_end_time = duration - 0.15
        audio_clip = audio_clip.subclip(0, new_end_time)
    
    return audio_clip 

def speed_up_audio(input_file, output_file, speed_factor=1.3):
    """
    Speed up the audio file by the specified speed factor using time stretching.

    Args:
        input_file (str): The path to the input audio file.
        output_file (str): The path to the output audio file.
        speed_factor (float): The speed factor by which to speed up the audio (default: 1.3).
    """
    # Load audio file
    audio = AudioSegment.from_file(input_file, format="mp3")
    
    # Calculate new duration of audio based on the speed factor
    new_duration = int(len(audio) / speed_factor)
    
    # Use time stretching to change audio duration
    sped_up_audio = audio.set_frame_rate(int(audio.frame_rate * speed_factor)).set_sample_width(2)
    sped_up_audio = sped_up_audio[:new_duration]
    
    # Export sped-up audio to a new file
    sped_up_audio.export(output_file, format="mp3")
