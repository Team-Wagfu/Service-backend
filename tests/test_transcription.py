"""
test audio file transciptions
"""

from openai import OpenAI


def test_audio():
    client = OpenAI()
    audio_file = open("./AudioRes/1.ogg", "rb")

    t = client.audio.transcriptions.create(model="gpt-4o-transcribe", file=audio_file)

    print(t.text)
