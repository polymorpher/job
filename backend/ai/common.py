from typing import List
import os
from ai.data import Resume
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

SYSTEM_PROMPT_BACKGROUND = '''You are a recommender, determining which candidates will match the job description.'''

SYSTEM_PROMPT_INSTRUCTION = '''Please recommend the top 3 candidates from the list below. Provide an explanation, focus on their achievements, skills, experience, education, and culture-fit. Show their location.'''

JOB_DESC_REPLACER = '{{job}}'
CANDIDATES_REPLACER = '{{candidates}}'

SINGLE_PROMPT = f'''{SYSTEM_PROMPT_BACKGROUND}

Job description: {JOB_DESC_REPLACER}

{SYSTEM_PROMPT_INSTRUCTION}

{CANDIDATES_REPLACER}
'''


def resume_to_list_item_text(r: Resume, prefix: str = '- ') -> str:
    return f'====\n{prefix}{r["author"]}:\n----\n{r["text"]}\n====\n'


def generate_single_prompt(job_text: str, resumes: List[Resume]) -> str:
    prompt = SINGLE_PROMPT.replace(JOB_DESC_REPLACER, job_text)
    resumes_texts = [resume_to_list_item_text(r) for r in resumes]
    flattened_resumes = '\n'.join(resumes_texts)
    prompt = prompt.replace(CANDIDATES_REPLACER, flattened_resumes)
    return prompt
