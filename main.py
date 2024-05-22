import audio
import background_video
import os
import reddit
import praw
import tempfile
import subtitles
import argparse
from pydub import AudioSegment
from moviepy.editor import ImageClip, VideoFileClip, concatenate_audioclips, AudioFileClip, CompositeVideoClip

def main():
    # Parse user arguments
    parser = argparse.ArgumentParser(description="Generate TikTok video from Reddit post")
    parser.add_argument("-s", "--subreddit", required=True, help="The name of the subreddit")
    parser.add_argument("-b", "--bg_video_file", required=True, help="Path to the background video file")
    parser.add_argument("-i", "--sessionID", required=True, help="TikTok session ID for text-to-speech")
    parser.add_argument("-t", "--time", default="all", help="Time range for the Reddit post (e.g., 'day', 'week', 'month', 'year', 'all')")
    parser.add_argument("-f", "--fps", type=int, default=60, help="Frames per second for the output video")
    parser.add_argument("-o", "--output_file_name", default="final_output.mp4", help="Name of the output video file")
    parser.add_argument("-c", "--custom_url", default=None, help="Custom URL of a Reddit post")
    parser.add_argument("-v", "--voice", default="en_us_002", help="Voice for text-to-speech. Check voices.py for full list")
    parser.add_argument("-m", "--max_words_on_screen", type=int, default=5, help="Maximum number of words allowed on the screen at one time")

    args = parser.parse_args()

    # Assign args to local variables
    subreddit = args.subreddit
    bg_video_file = args.bg_video_file
    sessionID = args.sessionID
    time = args.time
    fps = args.fps
    output_file_name = args.output_file_name
    custom_url = args.custom_url
    voice = args.voice
    max_words_on_screen = args.max_words_on_screen

    # subreddit = "NoStupidQuestions"
    # bg_video_file = "lowres.mp4"
    # fps = 60
    # output_file_name = "final_output.mp4"
    # time = "all"
    # custom_url = "https://www.reddit.com/r/NoStupidQuestions/comments/snppah/what_are_florida_ounces/"
    # voice = 'en_us_rocket'
    # max_words_on_screen = 5

    # Initialize the Reddit API client using environment variables
    reddit_api_key = os.environ.get("REDDIT_API_KEY")
    reddit_client_id = os.environ.get("REDDIT_CLIENT_ID")
    reddit_user_agent = os.environ.get("REDDIT_USER_AGENT")

    client = praw.Reddit(
        client_secret=reddit_api_key,
        client_id=reddit_client_id,
        user_agent=reddit_user_agent
    )

    if custom_url:
        # Extract the title and text from the custom URL
        title, text = reddit.extract_post_from_url(client, custom_url)
        url = custom_url
    else:
        # Find a top Reddit post from the specified subreddit
        title, text, url = reddit.find_post(client, subreddit, time)

    # Capture a screenshot of the Reddit post title, save screenshot to title.png
    reddit.capture_reddit_title_screenshot(url)

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

    # Generate the background video with the combined audio
    background_video.get_background_video(combined_audio_clip, bg_video_file, fps=fps)

    # Run the subtitle generator with temp files to avoid garbage collection
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        with tempfile.NamedTemporaryFile(suffix=".srt") as temp_subtitle:
            # Generate subtitles for the non-title part of the video
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

    # Combine the main video and logo into a final composite video named by user
    final_video = CompositeVideoClip([main_video, screenshot.set_start(0)])  
    final_video.write_videofile(filename=output_file_name, codec='libx264', audio_codec='aac', fps=fps)

    # Clean up temporary files
    try:
        os.remove('title.png')
        os.remove('output.mp4')
        os.remove('cropped.mp4')
        os.remove('output_video.mp4')
    except:
        pass

if __name__ == "__main__":
    main()
