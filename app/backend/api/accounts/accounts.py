from typing import List

from fastapi import APIRouter

from api import crud
from models.summaries.pydantic import SummaryPayloadSchema, SummaryResponseSchema
from models.summaries.tortoise import SummarySchema

router = APIRouter()


