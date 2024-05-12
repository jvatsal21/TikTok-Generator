# TikTok Generator
Automate TikToks from Reddit, comes with background video, music, text-to-speech, and automatic captioning!

<p align="center" width="100%">
</p>

### Demo
*insert demo vid*

### How To Use
1) Clone Repo
```
$ git clone https://github.com/jvatsal21/TikTok-Generator.git 
```
2) Download Requirements
```
$ pip install -r <project-directory>/requirements.txt
```
3) In reddit_text.py, update information with your Reddit API info

*If you do not have Reddit API use this link* https://www.reddit.com/prefs/apps
```
reddit = praw.Reddit(
    client_secret="REDDIT_API_KEY", #your Reddit API key
    client_id="REDDIT_CLIENT_ID",   #your Reddit Client ID
    user_agent="REDDIT_USER_AGENT"  #your Reddit user agent
)
```
4) Run generate_subtitles.py
```
$ python generate_subtitles.py
```
or
```
$ python3 generate_subtitles.py
```
5) Output should be in output-output.mp4

### Creators
**Developers:** Vatsal Joshi, Pranav Kante

