import math
import ffmpeg
import audio
import background_video

from faster_whisper import WhisperModel
from moviepy.editor import ColorClip, VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip


audio.generate_audio()
input_mp3 = "audio.mp3"
output_mp3 = "sped_up_audio.mp3"
audio.speed_up_audio(input_mp3, output_mp3, 1.3)

# Load the sped up audio file
audio_clip = AudioFileClip('sped_up_audio.mp3')

# Load the minecraft video file
background_video_clip = VideoFileClip('minecraft.mp4')

# Calculate the new dimensions to maintain a 9:16 aspect ratio
original_height = 1440
aspect_ratio = 9 / 16
new_width = int(original_height * aspect_ratio)

# Crop the video to the new dimensions centered on the middle
cropped_clip = background_video_clip.crop(x_center=background_video_clip.size[0]/2, width=new_width, height=original_height)
cropped_video_path = 'minecraft_cropped.mp4'
cropped_clip.write_videofile(cropped_video_path, codec='libx264', audio_codec='aac', fps=60, bitrate='8000k', preset='slow')

background_video_clip.close()

# Load the cropped video clip for further processing
background_clip = VideoFileClip(cropped_video_path)

# Set the duration of the background video to match the audio clip
background_clip = background_clip.subclip(0, audio_clip.duration)

# Set the audio of the video clip to be the sped-up audio clip
background_clip = background_clip.set_audio(audio_clip)

# Set the output file name
output_path = 'output_video.mp4'

# Write the result to a file (change codec and bitrate as needed)
background_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)

# Close all clips to clear memory
audio_clip.close()
background_clip.close()

input_video = "output_video.mp4"
input_video_name = input_video.replace(".mp4", "")


def extract_audio():
    extracted_audio = f"audio-{input_video_name}.wav"
    stream = ffmpeg.input(input_video)
    stream = ffmpeg.output(stream, extracted_audio)
    ffmpeg.run(stream, overwrite_output=True)
    return extracted_audio

def transcribe(audio):
    model = WhisperModel("small")
    segments, info = model.transcribe(audio)
    language = info[0]
    print("Transcription language", info[0])
    segments = list(segments)
    for segment in segments:
        # print(segment)
        print("[%.2fs -> %.2fs] %s" %
              (segment.start, segment.end, segment.text))
    return language, segments

def format_time(seconds):

    hours = math.floor(seconds / 3600)
    seconds %= 3600
    minutes = math.floor(seconds / 60)
    seconds %= 60
    milliseconds = round((seconds - math.floor(seconds)) * 1000)
    seconds = math.floor(seconds)
    formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:01d},{milliseconds:03d}"

    return formatted_time

def generate_subtitle_file(language, segments):

    subtitle_file = f"sub-{input_video_name}.{language}.srt"
    text = ""
    for index, segment in enumerate(segments):
        segment_start = format_time(segment.start)
        segment_end = format_time(segment.end)
        text += f"{str(index+1)} \n"
        text += f"{segment_start} --> {segment_end} \n"
        text += f"{segment.text} \n"
        text += "\n"
        
    f = open(subtitle_file, "w")
    f.write(text)
    f.close()

    return subtitle_file

def add_subtitle_to_video(soft_subtitle, subtitle_file,  subtitle_language):

    video_input_stream = ffmpeg.input(input_video)
    subtitle_input_stream = ffmpeg.input(subtitle_file)
    output_video = f"output-{input_video_name}.mp4"
    subtitle_track_title = subtitle_file.replace(".srt", "")

    if soft_subtitle:
        stream = ffmpeg.output(
            video_input_stream, subtitle_input_stream, output_video, **{"c": "copy", "c:s": "mov_text"},
            **{"metadata:s:s:0": f"language={subtitle_language}",
            "metadata:s:s:0": f"title={subtitle_track_title}"}
        )
        ffmpeg.run(stream, overwrite_output=True)
    else:
        stream = ffmpeg.output(video_input_stream, output_video,

                               vf=f"subtitles={subtitle_file}")

        ffmpeg.run(stream, overwrite_output=True)

def run():
    extracted_audio = extract_audio()
    language, segments = transcribe(audio=extracted_audio)
    subtitle_file = generate_subtitle_file(
    language=language,
    segments=segments
    )
    add_subtitle_to_video(
        soft_subtitle=False,
        subtitle_file=subtitle_file,
        subtitle_language=language
    )

run()