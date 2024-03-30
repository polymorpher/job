from typing import List
import google.generativeai as genai
import time
from ai.common import generate_single_prompt, GOOGLE_API_KEY
from ai.constants import TEST_JOB
from ai.data import Resume, load_resumes

genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel('gemini-pro')


def list_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


def find_matching_resumes(job_text: str, resumes: List[Resume] = [], n: int = 10) -> (str, str):
    if len(resumes) == 0:
        resumes = load_resumes(n=n, seed=int(time.time()))
    prompt = generate_single_prompt(job_text, resumes)
    result = MODEL.generate_content(prompt)
    return '', prompt, result.text


def main():
    # list_models()
    (system, prompt, response) = find_matching_resumes(job_text=TEST_JOB, n=100)
    print('SYSTEM: ', system)
    print('PROMPT: ', prompt)
    print('RESPONSE: ', response)


if __name__ == "__main__":
    main()
