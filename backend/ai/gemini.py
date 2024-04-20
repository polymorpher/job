from typing import List
import google.generativeai as genai
import time
from ai.common import GOOGLE_API_KEY, SYSTEM_PROMPT_BACKGROUND, JOB_DESC_REPLACER, CANDIDATES_REPLACER, \
    RECOMMEND_INSTRUCTION, resume_to_list_item_text, SYSTEM_PROMPT_REPLACER, make_instruction
from ai.constants import TEST_JOB
from ai.data import Resume, load_resumes

genai.configure(api_key=GOOGLE_API_KEY)
MODEL_LOOKUP = {
    "gemini-1.0": "gemini-1.0-pro-latest",
    "gemini-1.5": "gemini-1.5-pro-latest",
    "gemini": "gemini-1.5-pro-latest",
}

DEFAULT_MODEL = 'gemini'


def list_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


SINGLE_PROMPT = f'''{SYSTEM_PROMPT_BACKGROUND}

Job description: {JOB_DESC_REPLACER}

{SYSTEM_PROMPT_REPLACER}

{CANDIDATES_REPLACER}
'''


def generate_single_prompt(job_text: str, resumes: List[Resume], n: int) -> str:
    prompt = SINGLE_PROMPT.replace(JOB_DESC_REPLACER, job_text)
    system_prompt = make_instruction(n)
    prompt = prompt.replace(SYSTEM_PROMPT_REPLACER, system_prompt)
    resumes_texts = [resume_to_list_item_text(r) for r in resumes]
    flattened_resumes = '\n'.join(resumes_texts)
    prompt = prompt.replace(CANDIDATES_REPLACER, flattened_resumes)
    return prompt


def find_matching_resumes(job_text: str, resumes: List[Resume], n: int = 3, model=DEFAULT_MODEL) -> (str, str, str):
    if model in MODEL_LOOKUP:
        model = MODEL_LOOKUP[model]
    else:
        model = MODEL_LOOKUP[DEFAULT_MODEL]
    prompt = generate_single_prompt(job_text, resumes, n)
    gen_model = genai.GenerativeModel(model)
    result = gen_model.generate_content(prompt)
    return '', prompt, result.text


def main():
    # list_models()
    resumes = load_resumes(n=100, seed=int(time.time()))
    (system, prompt, response) = find_matching_resumes(job_text=TEST_JOB, resumes=resumes, n=3)
    print('SYSTEM: ', system)
    print('PROMPT: ', prompt)
    print('RESPONSE: ', response)


if __name__ == "__main__":
    main()
