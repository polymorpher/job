from typing import List

import google.generativeai as genai
from dotenv import load_dotenv
import os
import time

from ai.constants import TEST_JOB
from ai.data import Resume, load_resumes

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
MODEL = genai.GenerativeModel('gemini-pro')

BASE_PROMPT = '''You are a recommender, determining which candidates will match the job description.
Job description: {{job}}

Please recommend the top 3 candidates from the list below. Provide an explanation, focus on their achievements, skills, experience, education, and culture-fit. Show their location.

{{candidates}}
'''


def resume_to_list_item_text(r: Resume, prefix: str = '- ') -> str:
    return f'{prefix}{r["author"]}:\n----\n{r["text"]}\n----\n'


def generate_prompt(job_text: str, resumes: List[Resume]) -> str:
    prompt = BASE_PROMPT.replace('{{job}}', job_text)
    resumes_texts = [resume_to_list_item_text(r) for r in resumes]
    flattened_resumes = '\n'.join(resumes_texts)
    prompt = prompt.replace('{{candidates}}', flattened_resumes)
    return prompt


def list_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


def find_matching_resumes(job_text: str, resumes: List[Resume] = [], n: int = 10):
    if len(resumes) == 0:
        resumes = load_resumes(n=n, seed=int(time.time()))
    prompt = generate_prompt(job_text, resumes)
    print('PROMPT: ', prompt)
    result = MODEL.generate_content(prompt)
    print('RESPONSE: ', result.text)


def main():
    # list_models()
    find_matching_resumes(job_text=TEST_JOB, n=100)


if __name__ == "__main__":
    main()
