from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import ffmpeg


def get_minecraft_video(audio_clip):
    # Specify the path to your video file (background video)
    background_video_path = 'muted_video.mp4'
    
    # Load the video file
    background_video_clip = VideoFileClip(background_video_path)

    # Adjust the video clip's duration to match the audio clip's duration
    if background_video_clip.duration < audio_clip.duration:
        # If the background video is shorter, loop it
        loop_count = int(audio_clip.duration // background_video_clip.duration) + 1
        background_video_clip = concatenate_videoclips([background_video_clip] * loop_count)
        background_video_clip = background_video_clip.subclip(0, audio_clip.duration)
    else:
        # If the background video is longer, trim it
        background_video_clip = background_video_clip.subclip(0, audio_clip.duration)

    background_video_clip.set_audio(audio_clip)

    return background_video_clip