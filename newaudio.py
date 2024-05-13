from elevenlabs import generate, play

audio = generate(
    text="""I’ve taken note of your meetings for the day:
    you have a conference call with the design team at 10,
    followed by a client lunch at 1. Remember to review the
    project proposal before the call! I’ve also seen a few
    emails flagged for your attention in your inbox - would
    you like me to draft responses or schedule them for later?""",
    voice="Bella",
    model='eleven_monolingual_v1'
)

play(audio)