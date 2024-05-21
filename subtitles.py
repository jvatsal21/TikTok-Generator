import math
import ffmpeg
from faster_whisper import WhisperModel

def extract_audio(skip_seconds, input_video, output_audio):
    """
    Extract audio from a video file that needs subtitles.

    Args:
        skip_seconds (float): The duration of the title speech, which doesn't need subtitles.
        input_video (str): The path to the input video file.
        output_audio (str): The path to the output audio file.
    """
    stream = ffmpeg.input(input_video)

    # Use ffmpeg command to extract audio from video file not containing the title narration
    # We do not need subtitles for the title since we already display a screenshot of it
    stream = ffmpeg.output(stream, output_audio, ss=skip_seconds)
    ffmpeg.run(stream, overwrite_output=True)


def transcribe(audio_file):
    """
    Transcribe the audio from a file using the Whisper model.

    Args:
        audio_file (str): The path to the audio file.

    Returns:
        tuple: A list of transcribed segments.
    """
    # Using small for reasonable processing time
    model = WhisperModel("small")
    segments, info = model.transcribe(audio_file)
    # Outputs to terminal segments of detected speech
    print("Transcription language", info[0])
    segments = list(segments)
    for segment in segments:
        # Include timestamps of detected speech
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    return segments


def format_time(seconds):
    """
    Format the given time in seconds to a string in the format "HH:MM:SS,mmm".

    Args:
        seconds (float): The time in seconds.

    Returns:
        str: The formatted time string.
    """
    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"
    return formatted_time


def generate_subtitle_file(segments, title_duration, subtitle_file, max_words_on_screen):
    """
    Generate a subtitle file (srt) from the previously transcribed segments.

    Args:
        segments (list): The list of transcribed segments.
        title_duration (float): The duration of the title in seconds.
        subtitle_file (str): The path to the output subtitle file.
        max_words_on_screen (int): The maximum number of words allowed on the screen at a time.
    """
    text = ""
    subtitle_index = 1

    for segment in segments:
        words = segment.text.split()
        start_time = segment.start

        # Process the current segment text to fit the max_words_on_screen constraint
        while words:
            subtitle_words = words[:max_words_on_screen]
            subtitle_text = " ".join(subtitle_words)
            words = words[max_words_on_screen:]

            # Calculate end time for the current subtitle
            end_time = segment.end if not words else start_time + (segment.end - start_time) * len(subtitle_words) / (len(subtitle_words) + len(words))

            # Format times and build subtitle text
            segment_start = format_time(start_time + title_duration)
            segment_end = format_time(end_time + title_duration)

            text += f"{subtitle_index}\n"
            text += f"{segment_start} --> {segment_end}\n"
            text += f"{subtitle_text}\n\n"

            # Update start time for next subtitle and increment subtitle index in SRT file
            start_time = end_time
            subtitle_index += 1

    # Write subtitle content to file
    with open(subtitle_file, "w") as f:
        f.write(text)

def add_subtitle_to_video(subtitle_file, input_video, output_video):
    """
    Add stylized subtitles to the video file.

    Args:
        subtitle_file (str): The path to the subtitle file.
        input_video (str): The path to the input video file.
        output_video (str): The path to the output video file with subtitles.
        subtitle_language (str): The language of the subtitles.
    """
    video_input_stream = ffmpeg.input(input_video)
    # Use the ffmpeg force_style attribute to design an aesthetic font as well as make it centered on the screen
    stream = ffmpeg.output(
        video_input_stream,
        output_video,
        vf=f"subtitles={subtitle_file}:force_style='FontName=Komika Axis,FontSize=15,Alignment=10,Outline=2,OutlineColor=&H000000&'"
    )
    # Apply the stylized subtitles to the final video
    ffmpeg.run(stream, overwrite_output=True)


def run(title_duration, input_video, temp_audio, temp_subtitle, max_words_per_screen=5):
    """
    Run the subtitle generation process. Save final video as output.mp4.

    Args:
        title_duration (float): The duration of the title in seconds.
        input_video (str): The path to the input video file.
        temp_audio (tempfile.NamedTemporaryFile): A temporary file for storing the extracted audio.
        temp_subtitle (tempfile.NamedTemporaryFile): A temporary file for storing the generated subtitles.
        max_words_per_line (int): The maximum number of words allowed on the screen at a time. (default: 5).
    """
    # Step 1: Extract audio that needs subtitles
    extract_audio(title_duration, input_video, temp_audio.name)
    # Step 2: Convert audio into time-stamped segments of text
    segments = transcribe(temp_audio.name)
    # Step 3: Use these segments to make an SRT subtitle file
    generate_subtitle_file(segments, title_duration, temp_subtitle.name, max_words_per_screen)
    # Step 4: Add the subtitles along with styles to the final video 
    add_subtitle_to_video(temp_subtitle.name, input_video, "output.mp4")