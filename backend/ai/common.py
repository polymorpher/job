from typing import List
import os
from ai.data import Resume
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

SYSTEM_PROMPT_BACKGROUND = '''You are a recommender, determining which candidates will match the job description.'''

CANDIDATE_COUNT_REPLACER = '{{candidate_count}}'

RECOMMEND_INSTRUCTION = f'''Please recommend the top {CANDIDATE_COUNT_REPLACER} candidates from the list below. Provide an explanation, focus on their achievements, skills, experience, education, and culture-fit. Show their location.'''

JOB_DESC_REPLACER = '{{job}}'
CANDIDATES_REPLACER = '{{candidates}}'
SYSTEM_PROMPT_REPLACER = '{{system_prompt}}'


def make_instruction(num_candidate: int = 3) -> str:
    return RECOMMEND_INSTRUCTION.replace(CANDIDATE_COUNT_REPLACER, str(num_candidate))


def resume_to_list_item_text(r: Resume, prefix: str = '- ') -> str:
    return f'====\n{prefix}{r["author"]}:\n----\n{r["text"]}\n====\n'
