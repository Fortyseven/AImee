# AImee

AImee is a realtime LLM conversation bot using Ollama, RealtimeTTS and RealtimeSTT, all of which are built on top of OTHER projects. It's just shoulders all the way down.

This is a terminal app that listens to the currently enabled microphone, transcribes your audio, passes it through to an LLM (maintaining a context window), and then speaks the response.

On a 4090 this can all go pretty fast. Enough to have a reasonable conversation. Though, the system prompting tries to make sure it doesn't give overly verbose responses.

This is just a silly toy project. Use it to make your own. Whatever. :)

I am offering no support for this project.

## Notes and Things To Fix

- Missing: you cannot interrupt the response.
- If you pause too long while talking it will auto-submit and cut you off. But once you begin speaking again, while it's processing, it will treat that like the next bit of dialogue. This is a bug.
- This could use a cleaner TUI.
- Proper command line arguments: currently you just edit the constants at the top of `main.py`.

## Project Structure

- `sprompts` contains Yaml files defining various personalities. Yaml, the devil's config file, was chosen because it fits the multiline prompt situation much better than JSON. I did not look at Toml. Maybe that's even better.

  - keys:
    - `prompt`: the system prompt itself
    - `user`: overrides the default user description
    - `temperature`: this has not been implemented yet; it's trivial, why am I slacking...?

- `sprompts/_user.default.yml` is the user injected into the sprompt if `user` is not defined

- `voices` are wav files that Coqui uses to clone voices. You can provide your own. It's not perfect, but it's fun.

## Requirements

- Python >= 3.12 (this is not a hard requirement; just what I used)

## Usage

- Do the usual Python dance: venv, requirements, etc.

- I use a `Makefile` to just type `make` and go. I did this because, if you look inside, I'm overriding LD_LIBRARY_PATH to include a path to a shared file that isn't being referenced properly. This may not be required in your case. Or may not be relevant in future versions. Hell, it may even break something later.
