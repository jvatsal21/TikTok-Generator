# TikTok Generator
Automate TikToks from Reddit, comes with background video, music, text-to-speech, and automatic captioning!

<p align="center" width="100%">
</p>

## Demo
[*demo vid*](https://www.tiktok.com/@roboredditor/video/7371535112929824043?_r=1&_t=8oDKOYOF0cY)
*This is from our demo account the official account got banned lol

## How To Use (With Docker)

Make sure Docker is installed

*information to install docker* https://docs.docker.com/get-docker/

1) Clone Repo
```
$ git clone https://github.com/jvatsal21/TikTok-Generator.git 
```
2) Edit .env to contain the appropriate keys: Reddit API: https://www.reddit.com/prefs/apps , TikTok Session_id you can get from your account
```
REDDIT_API_KEY= YOUR_REDDIT_API_KEY
REDDIT_CLIENT_ID= YOUR_REDDIT_CLIENT_ID
REDDIT_USER_AGENT= YOUR_REDDIT_USER_AGENT
TIKTOK_SESSION_ID= YOUR_TIKTOK_SESSION_ID
```
3) Update config.json for your desired configurations

*If you do not have Reddit API use this link* https://www.reddit.com/prefs/apps
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
4) Add your mp4 file(the video you want to put in the background) in the assets folder 
5) Run docker
```
$ docker-compose up --build
```


## Credits
**TikTok Text-to-speech API**: https://github.com/oscie57/tiktok-voice

## Creators
**Developers:** Vatsal Joshi, Pranav Kante
