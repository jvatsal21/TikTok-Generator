from moviepy.editor import VideoFileClip

def get_background_video(audio_clip, video_clip, fps):
    """
    Generate a video with the given audio clip and background video.

    Args:
        audio_clip (AudioFileClip): The audio clip to be used as the audio for the video.
        video_clip (str): The path to the background video file.
        fps (int): The frames per second for the output video.
    """
    # Convert background video (.mp4) to VideoFileClip format
    background_video_clip = VideoFileClip(video_clip)

    # Crop the background to TikTok's 9:16 aspect ratio
    original_height = background_video_clip.size[1]
    aspect_ratio = 9 / 16
    new_width = int(original_height * aspect_ratio)

    cropped_clip = background_video_clip.crop(x_center=background_video_clip.size[0]/2, width=new_width, height=original_height)
    cropped_video_path = 'cropped.mp4'
    cropped_clip.write_videofile(cropped_video_path, codec='libx264', audio_codec='aac', fps=fps, bitrate='8000k', preset='slow')
    background_video_clip.close()

    # Load the cropped video clip, and set the audio of the background clip to provided audio clip
    background_clip = VideoFileClip(cropped_video_path)
    background_clip = background_clip.subclip(0, audio_clip.duration)
    background_clip = background_clip.set_audio(audio_clip)

    # Write the final video to an output file for later use
    output_path = 'output_video.mp4'
    background_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=fps)

    # Close files at end
    audio_clip.close()
    background_clip.close()
