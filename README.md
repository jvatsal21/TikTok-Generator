# 🎥 TikTok Generator
Make the trendiest TikToks in minutes. Our editor will automatically generate background video, text-to-speech, and captions, all you have to do it drop a funny reddit post.

## 📌 About This Project
Content creation is hard and takes lots of time. This tool automates the process of creating TikTok videos from Reddit posts. Given a subreddit or a specific Reddit post, it extracts the top post content, overlays text on a background video, adds text-to-speech narration, and generates a fully edited TikTok-ready video. 

Our goal was to create a fully automated content pipeline that allows creators to generate engaging TikTok videos without manually editing clips, adding captions, or recording voiceovers. This is particularly useful for meme pages, content creators, and automation enthusiasts who want to streamline TikTok content creation.

## 🚀 Demo

https://github.com/user-attachments/assets/05327a21-a072-42ae-a605-1684946628f8

## 🛠️ Setup & Usage (Docker)

### Prerequisites
Make sure **Docker** is installed: [Get Docker](https://docs.docker.com/get-docker/)

### Step 1: Clone the Repository

```
$ git clone https://github.com/jvatsal21/TikTok-Generator.git 
```

### Step 2: Configure Environment Variables
Create a `.env` file and add your **Reddit API keys** and **TikTok session ID**.

- Get your **Reddit API keys**: [Reddit Apps](https://www.reddit.com/prefs/apps)
- Find your **TikTok session ID** from your account cookies.
  
Your `.env` file should look like this: 
```
REDDIT_API_KEY=<YOUR_REDDIT_API_KEY>
REDDIT_CLIENT_ID=<YOUR_REDDIT_CLIENT_ID>
REDDIT_USER_AGENT=<YOUR_REDDIT_USER_AGENT>
TIKTOK_SESSION_ID=<YOUR_TIKTOK_SESSION_ID>
```

### Step 3: Customize Configuration
Modify `config.json` to set your preferences:

```
{
  "bg_video_file": "any mp4 video",
  "subreddit": "",
  "time": "",
  "fps": "60",
  "output_file_name": "",
  "custom_url": "reddit url",
  "voice": "",
  "max_words_on_screen": ""
}
```
📌 **Note:** If you don’t have Reddit API keys, use [this link](https://www.reddit.com/prefs/apps).

### Step 4: Add Background Video
Place your **background video (MP4 file)** inside the `assets/` folder.

### Step 5: Run with Docker
4) Add your mp4 file(the video you want to put in the background) in the assets folder 
5) Run docker
```
$ docker-compose up --build
```

## 💡 How It Works
1. **Fetch Reddit Post**: Retrieves a top post from a given subreddit or custom URL.
2. **Extract Content**: Parses post text and formats it for TikTok display.
3. **Generate Captions**: Adds automatic on-screen captions.
4. **Text-to-Speech**: Converts text to speech using TikTok’s voice API.
5. **Merge with Background Video**: Overlays text and speech onto a chosen MP4 background.
6. **Export Ready-to-Post Video**: Outputs a final TikTok-ready video.

## 🤝 Credits
- **TikTok Text-to-Speech API**: [osc57/tiktok-voice](https://github.com/oscie57/tiktok-voice)

## 👥 Creators
**Developers:**  
- [Vatsal Joshi](https://github.com/jvatsal21)  
- [Pranav Kante](https://github.com/pkante)
