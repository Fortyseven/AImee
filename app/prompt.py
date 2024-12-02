import yaml

PROMPT_PATH = "sprompts"


def load_prompt(prompt_name):
    # load yaml prompt
    with open(f"{PROMPT_PATH}/{prompt_name}.yml", "r") as f:
        prompt = yaml.safe_load(f)

    return prompt
