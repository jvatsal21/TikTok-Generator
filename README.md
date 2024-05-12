# Automate Reddit TikTok Videos 

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
```
reddit = praw.Reddit(
    client_secret=os.environ["REDDIT_API_KEY"],
    client_id=os.environ["REDDIT_CLIENT_ID"],
    user_agent=os.environ["REDDIT_USER_AGENT"]
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

