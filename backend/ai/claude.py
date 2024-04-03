import time
from typing import List

from anthropic import Anthropic

from ai.common import SYSTEM_PROMPT_BACKGROUND, resume_to_list_item_text, RECOMMEND_INSTRUCTION, ANTHROPIC_API_KEY, \
    CANDIDATE_COUNT_REPLACER
from ai.constants import TEST_JOB
from ai.data import Resume, load_resumes

client = Anthropic(api_key=ANTHROPIC_API_KEY)

MODEL_LOOKUP = {
    "opus": "claude-3-opus-20240229",
    "sonnet": "claude-3-sonnet-20240229",
    "haiku": "claude-3-haiku-20240307",
}

DEFAULT_MODEL = "opus"


def find_matching_resumes(job_text: str, resumes: List[Resume], n: int = 3, model=DEFAULT_MODEL):
    if model in MODEL_LOOKUP:
        model = MODEL_LOOKUP[model]
    else:
        model = MODEL_LOOKUP[DEFAULT_MODEL]

    system = f'{SYSTEM_PROMPT_BACKGROUND}\nJob description: {job_text}'
    resumes_texts = [resume_to_list_item_text(r) for r in resumes]
    flattened_resumes = '\n'.join(resumes_texts)
    instruction = RECOMMEND_INSTRUCTION.replace(CANDIDATE_COUNT_REPLACER, str(n))
    prompt = f'{instruction}\n\n{flattened_resumes}'

    message = client.messages.create(
        model=model,
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
    resumes = load_resumes(n=100, seed=int(time.time()))
    (system, prompt, response) = find_matching_resumes(job_text=TEST_JOB, resumes=resumes, n=3)
    print('SYSTEM: ', system)
    print('PROMPT: ', prompt)
    print('RESPONSE: ', response)


if __name__ == "__main__":
    main()
