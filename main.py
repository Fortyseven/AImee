#!/usr/bin/env python3

import time
from rich import print

from RealtimeSTT import AudioToTextRecorder
from RealtimeTTS import TextToAudioStream, CoquiEngine
from ollama import chat

from app.prompt import load_prompt


SPROMPT = "lcars"
VOICE_FILE = "fem1"
LLM_MODEL = "llama3.1:latest"  # llama 3.1 8B is great a following directions, so I default to that; YMMV

stream = None

messages = []


def process_text(text):
    global messages

    print(f"\n----\n[red]User:[/red] {text}")

    # tack it on the end, send it up
    messages.append({"role": "user", "content": text})

    response = chat(LLM_MODEL, messages=messages)

    # tack their response onto the end for the next go-around
    messages.append(response["message"])

    resp = response["message"]["content"]

    print(f"\n[blue]Resp:[/blue] {resp}\n")

    # say the response
    stream.feed(resp)
    stream.play_async()

    while stream.is_playing():
        time.sleep(0.1)


def on_audio_stream_start():
    recorder.set_microphone(False)


def on_audio_stream_stop():
    recorder.set_microphone(True)


if __name__ == "__main__":
    sprompt = load_prompt(SPROMPT)

    # allow overrides from the sprompt

    voice = sprompt["voice"] or VOICE_FILE

    if not sprompt["user"]:
        user = load_prompt("_user.default")
        user = user["prompt"]
    else:
        user = sprompt["user"]

    today = time.strftime("%A, %B %d, %Y")

    messages.append(
        {
            "role": "system",
            "content": f"{sprompt["prompt"]}\n####\nAbout the user:\n{user}####\nToday is {today}.",
        }
    )

    print(f"- Using prompt: `{SPROMPT}`")

    engine = CoquiEngine(voice=f"voices/{voice}.wav")

    stream = TextToAudioStream(
        engine,
        # if we don't do this, it will likely hear
        # itself and respond over and over. which
        # may be fun in a noisy environment, but
        # not right now.
        on_audio_stream_start=on_audio_stream_start,
        on_audio_stream_stop=on_audio_stream_stop,
    )

    recorder = AudioToTextRecorder()

    while True:
        if not stream.is_playing():
            recorder.text(process_text)
