import audio
import background_video
import os
import reddit
import utils
import tempfile
import subtitles
from pydub import AudioSegment
from moviepy.editor import ImageClip, VideoFileClip, concatenate_audioclips, AudioFileClip, CompositeVideoClip

def main():
    print("\nBeginning video creation...\n___________\n")

    # Check if environment variables were inputted
    utils.load_and_check_env()

    # Check if the config file is provided and exists
    config_file = 'config.json'
    config = utils.read_config(config_file) if os.path.exists(config_file) else {}
    
    args = utils.parse_arguments(config)
    sessionID = os.getenv('TIKTOK_SESSION_ID')

    # Assign args to local variables
    subreddit = args.subreddit
    bg_video_file = args.bg_video_file
    time = args.time
    fps = args.fps
    output_file_name = args.output_file_name
    custom_url = args.custom_url
    voice = args.voice
    max_words_on_screen = args.max_words_on_screen

    client = utils.initialize_reddit_client()

    if custom_url:
        # Extract the title and text from the custom URL
        title, text = reddit.extract_post_from_url(client, custom_url)
        url = custom_url
    else:
        # Find a top Reddit post from the specified subreddit
        title, text, url = reddit.find_post(client, subreddit, time)

    # Capture a screenshot of the Reddit post title, save screenshot to title.png
    reddit.capture_reddit_title_screenshot(url)

    print("Generating voiceover\n___________\n")

    # Generate audio for the post title & text
    title_audio_clip = audio.generate_audio(title, sessionID, voice, True)
    main_audio_clip = audio.generate_audio(text, sessionID, voice, False)
    
    # Make a brief silent audio clip to have a pause at the end of the video
    silent_audio = AudioSegment.silent(duration=1500)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_silent_audio:
        silent_audio.export(temp_silent_audio.name, format="wav")
        silent_clip = AudioFileClip(temp_silent_audio.name)

    # Combine the audio clips with the silent clip after
    combined_audio_clip = concatenate_audioclips([title_audio_clip, main_audio_clip, silent_clip])
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_combined_audio:
        combined_audio_clip.write_audiofile(temp_combined_audio.name)

    print("\nCombining background video with voiceover...\n___________\n")
    # Generate the background video with the combined audio
    background_video.get_background_video(combined_audio_clip, bg_video_file, fps=fps)

    print("\nGenerating subtitles...\n___________\n")
    # Run the subtitle generator with temp files to avoid garbage collection
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio, tempfile.NamedTemporaryFile(suffix=".srt") as temp_subtitle:
        subtitles.run(title_audio_clip.duration, "output_video.mp4", temp_audio, temp_subtitle, max_words_on_screen)

    # Load the main video clip one last time to add the screenshot
    main_video = VideoFileClip("output.mp4")
    screenshot = ImageClip('title.png')

    # Set the duration of the logo to match the title audio duration
    screenshot = screenshot.set_duration(title_audio_clip.duration) 
    
    # Resize the screenshot to make it fit in the center of the video
    scale_factor = 0.9 * main_video.size[0] / screenshot.size[0]
    screenshot = screenshot.resize(scale_factor)
    screenshot = screenshot.set_pos('center') 

    print("\nFinishing up final video...\n___________\n")
    
    # Combine the main video and logo into a final composite video named by user
    final_video = CompositeVideoClip([main_video, screenshot.set_start(0)])  
    final_video.write_videofile(filename=output_file_name, codec='libx264', audio_codec='aac', fps=fps)

    # Clean up temporary files
    for temp_file in ['title.png', 'output.mp4', 'cropped.mp4', 'output_video.mp4']:
        try:
            os.remove(temp_file)
        except:
            pass

if __name__ == "__main__":
    main()