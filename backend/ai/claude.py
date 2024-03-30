import time
from typing import List

from anthropic import Anthropic

from ai.common import SYSTEM_PROMPT_BACKGROUND, resume_to_list_item_text, SYSTEM_PROMPT_INSTRUCTION, ANTHROPIC_API_KEY
from ai.constants import TEST_JOB
from ai.data import Resume, load_resumes

client = Anthropic(api_key=ANTHROPIC_API_KEY)

# MODEL_NAME = "claude-3-opus-20240229"
# MODEL_NAME = "claude-3-sonnet-20240229"
MODEL_NAME = "claude-3-haiku-20240307"


def find_matching_resumes(job_text: str, resumes: List[Resume] = [], n: int = 10):
    if len(resumes) == 0:
        resumes = load_resumes(n=n, seed=int(time.time()))
    system = f'{SYSTEM_PROMPT_BACKGROUND}\nJob description: {job_text}'
    resumes_texts = [resume_to_list_item_text(r) for r in resumes]
    flattened_resumes = '\n'.join(resumes_texts)
    prompt = f'{SYSTEM_PROMPT_INSTRUCTION}\n\n{flattened_resumes}'

    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        system=system,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    response = '\n\n'.join([t.text for t in message.content])
    return (system, prompt, response)


def main():
    # list_models()
    (system, prompt, response) = find_matching_resumes(job_text=TEST_JOB, n=100)
    print('SYSTEM: ', system)
    print('PROMPT: ', prompt)
    print('RESPONSE: ', response)


if __name__ == "__main__":
    main()
