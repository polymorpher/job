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


def load_freelancers_and_tasks(n: int, seed_worker: int = 0, seed_jobs: int = 0):
    listings = all_data['freelancer']
    workers = listings.filter(lambda p: str(p['text']).upper().startswith(SEEKING_WORK)).map(
        lambda p: {'text': trim_text_leading_punc(p['text'][len(SEEKING_WORK):])}
    )
    jobs = listings.filter(lambda p: str(p['text']).upper().startswith(SEEKING_FREELANCERS)).map(
        lambda p: {'text': trim_text_leading_punc(p['text'][len(SEEKING_FREELANCERS):])}
    )
    return workers.shuffle(seed_worker)[:n], jobs.shuffle(seed_jobs)[:n]


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
    # (workers, jobs) = load_freelancers_and_tasks(5)
    # print(workers['text'])
    # print(load_resumes(5))
    print(load_jobs(1))


if __name__ == "__main__":
    main()
