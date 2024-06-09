import os
import sys
import json
import praw
import argparse
from dotenv import load_dotenv

def read_config(config_file):
    """
    Read the JSON configuration file.

    Parameters:
    - config_file (str): Path to the configuration file.

    Returns:
    - dict: Configuration as a dictionary.
    """
    with open(config_file, 'r') as file:
        return json.load(file)

def get_config_value(key, config, default_values):
    """
    Get a value from the configuration with a fallback to default values.

    Parameters:
    - key (str): The configuration key.
    - config (dict): The configuration dictionary.
    - default_values (dict): Default values dictionary.

    Returns:
    - Any: The value from the configuration or default values.
    """
    value = config.get(key, "")
    return default_values.get(key, "") if value in ["", "default"] else value

def check_env_variables(required_vars):
    """
    Check if required environment variables are set.

    Parameters:
    - required_vars (list): List of required environment variable names.

    Raises:
    - SystemExit: If any required environment variables are missing.
    """
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        sys.stderr.write(f"Error: Missing required environment variables: {', '.join(missing_vars)}\n")
        sys.exit(1)

def load_and_check_env():
    """
    Load environment variables from .env file and check required variables.
    """
    load_dotenv()
    required_env_vars = ["REDDIT_API_KEY", "REDDIT_CLIENT_ID", "REDDIT_USER_AGENT", "TIKTOK_SESSION_ID"]
    check_env_variables(required_env_vars)

def parse_arguments(config):
    """
    Parse command-line arguments.

    Parameters:
    - config (dict): Configuration dictionary.

    Returns:
    - argparse.Namespace: Parsed arguments.
    """
    default_values = {
        "time": "all",
        "fps": 60,
        "output_file_name": "final_output.mp4",
        "custom_url": "",
        "voice": "en_us_002",
        "max_words_on_screen": 5
    }

    parser = argparse.ArgumentParser(description="Generate TikTok video from Reddit post")
    parser.add_argument("-b", "--bg_video_file", default=config.get("bg_video_file", ""), help="Path to the background video file")
    parser.add_argument("-c", "--custom_url", default=config.get("custom_url", ""), help="Custom URL of a Reddit post")
    parser.add_argument("-s", "--subreddit", default=config.get("subreddit", ""), help="The name of the subreddit")
    parser.add_argument("-t", "--time", default=get_config_value("time", config, default_values), help="Time range for the Reddit post")
    parser.add_argument("-f", "--fps", type=int, default=get_config_value("fps", config, default_values), help="Frames per second for the output video")
    parser.add_argument("-o", "--output_file_name", default=get_config_value("output_file_name", config, default_values), help="Name of the output video file")
    parser.add_argument("-v", "--voice", default=get_config_value("voice", config, default_values), help="Voice for text-to-speech. Check voices.py for full list")
    parser.add_argument("-m", "--max_words_on_screen", type=int, default=get_config_value("max_words_on_screen", config, default_values), help="Maximum number of words allowed on the screen at one time")

    args = parser.parse_args()

    missing_args = []
    if not args.bg_video_file:
        missing_args.append("bg_video_file")
    if not args.custom_url and not args.subreddit:
        missing_args.append("(subreddit OR custom_url)")

    if missing_args:
        sys.stderr.write(f"Error: Missing required arguments: {', '.join(missing_args)}\n")
        sys.exit(1)

    if bool(args.custom_url) == bool(args.subreddit):
        sys.stderr.write("Error: You must provide either a custom_url or a subreddit, but not both.\n")
        sys.exit(1)

    return args

def initialize_reddit_client():
    """
    Initialize the Reddit API client using environment variables.

    Returns:
    - praw.Reddit: Initialized Reddit API client.
    """
    return praw.Reddit(
        client_secret=os.getenv("REDDIT_API_KEY"),
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        user_agent=os.getenv("REDDIT_USER_AGENT")
    )