from typing import TypedDict
from datetime import datetime
from datasets import load_from_disk
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class Resume(TypedDict):
    text: str
    author: str
    time: datetime


class Job(TypedDict):
    text: str
    author: str
    time: datetime


def load_all_data():
    dataset = load_from_disk(f'{dir_path}/../../hackernews_hiring_posts/data')
    return dataset


all_data = load_all_data()


def trim_text_leading_punc(text: str):
    text = text.strip()

    if text.startswith('--'):
        text = text[2:].strip()

    if text.startswith(('-', ' ', ':', ',', '|')):
        text = text[1:].strip()

    return text.strip()


SEEKING_WORK = 'SEEKING WORK'
SEEKING_FREELANCERS = 'SEEKING FREELANCERS'

freelance_workers = all_data['freelancer'].filter(lambda p: str(p['text']).upper().startswith(SEEKING_WORK)).map(
    lambda p: Resume(
        text=trim_text_leading_punc(p['text'][len(SEEKING_WORK):]),
        author=p['CommentAuthor'],
        time=datetime.strptime(p['CommentTime'], '%Y-%m-%d %H:%M:%S UTC')
    )
)

freelance_jobs = all_data['freelancer'].filter(lambda p: str(p['text']).upper().startswith(SEEKING_FREELANCERS)).map(
    lambda p: Resume(
        text=trim_text_leading_punc(p['text'][len(SEEKING_FREELANCERS):]),
        author=p['CommentAuthor'],
        time=datetime.strptime(p['CommentTime'], '%Y-%m-%d %H:%M:%S UTC')
    )
)


def load_freelancers_jobs(n: int, seed_jobs: int = 0):
    return freelance_jobs.shuffle(seed_jobs)[:n]


def load_freelancers_workers(n: int, seed_worker: int = 0):
    return freelance_workers.shuffle(seed_worker)[:n]


def load_jobs(n, seed=0):
    jobs = all_data['hiring']
    samples = jobs.shuffle(seed)[:n]
    dicts = [dict(zip(samples, t)) for t in zip(*samples.values())]
    return [Job(text=t['text'], author=t['CommentAuthor'],
                time=datetime.strptime(t['CommentTime'], '%Y-%m-%d %H:%M:%S UTC')) for t in dicts]


def load_resumes(n, seed=0):
    wants_to_be_hired = all_data['wants_to_be_hired']
    samples = wants_to_be_hired.shuffle(seed)[:n]
    dicts = [dict(zip(samples, t)) for t in zip(*samples.values())]
    return [Resume(text=t['text'], author=t['CommentAuthor'],
                   time=datetime.strptime(t['CommentTime'], '%Y-%m-%d %H:%M:%S UTC')) for t in dicts]


def main():
    # workers = load_freelancers_workers(5)
    # print(workers['text'])
    # print(load_resumes(5))
    print(load_jobs(1))


if __name__ == "__main__":
    main()
