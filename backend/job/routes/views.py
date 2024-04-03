from typing import List

import requests
import json
import os

from django.http import HttpResponse, HttpRequest
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from pydantic import BaseModel, ValidationError

from ai.data import Resume, load_resumes, load_freelancers_workers
from ai.gemini import find_matching_resumes as gemini_match
from ai.claude import find_matching_resumes as claude_match

from dotenv import load_dotenv

load_dotenv()

default_model = os.getenv('DEFAULT_MODEL')


class SimpleCandidateMatchRequest(BaseModel):
    job_description: str
    resume_source_id: str = 'hackernews_want_to_be_hired'
    resume_rng_seed: int = 0
    nun_random_candidates_sampled: int = 500
    num_candidate_requested: int = 3
    preferred_model: str = default_model


def ping(request):
    data = {status: True}
    return HttpResponse("pong", content_type="text/plain")


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def recommend_resume(request: HttpRequest):
    try:
        match_request = SimpleCandidateMatchRequest(**request.body)
    except ValidationError as e:
        return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": e.errors()})
    resumes: List[Resume] = []
    if match_request.resume_source_id == 'hackernews_want_to_be_hired':
        resumes = load_resumes(n=match_request.nun_random_candidates_sampled, seed=match_request.resume_rng_seed)
    elif match_request.resume_source_id == 'hackernews_freelance_seeking_work':
        resumes = load_freelancers_workers(n=match_request.nun_random_candidates_sampled,
                                           seed=match_request.resume_rng_seed)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={"error": "invalid resume_source_id", "resume_source_id": match_request.resume_source_id})

    if match_request.preferred_model == 'gemini':
        (system, instruction, response) = gemini_match(job_text=match_request.job_description, resumes=resumes,
                                                       n=match_request.nun_random_candidates_sampled)
    else:
        (system, instruction, response) = claude_match(job_text=match_request.job_description, resumes=resumes,
                                                       n=match_request.nun_random_candidates_sampled,
                                                       model=match_request.preferred_model)

    print(f'REQUEST: {match_request}')
    print(f'SYSTEM: {system}')
    print(f'INSTRUCTION: {instruction}')
    print(f'RESPONSE: {response}')
    return Response(status=status.HTTP_200_OK, data={"response": response})
