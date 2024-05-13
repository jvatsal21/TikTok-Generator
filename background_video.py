from moviepy.editor import VideoFileClip, CompositeVideoClip, concatenate_videoclips
import ffmpeg


def get_minecraft_video(audio_clip, video_clip):
    
    background_video_clip = VideoFileClip(video_clip)

    original_height = background_video_clip.size[1]
    aspect_ratio = 9 / 16
    new_width = int(original_height * aspect_ratio)

    cropped_clip = background_video_clip.crop(x_center=background_video_clip.size[0]/2, width=new_width, height=original_height)
    cropped_video_path = 'cropped.mp4'
    cropped_clip.write_videofile(cropped_video_path, codec='libx264', audio_codec='aac', fps=60, bitrate='8000k', preset='slow')
    background_video_clip.close()

    background_clip = VideoFileClip(cropped_video_path)
    background_clip = background_clip.subclip(0, audio_clip.duration)
    background_clip = background_clip.set_audio(audio_clip)

    output_path = 'output_video.mp4'
    background_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=60)

    audio_clip.close()
    background_clip.close()
