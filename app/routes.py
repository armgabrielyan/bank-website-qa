from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from app.pipeline import answer_question
from app.schemas import Answer, Question

router = APIRouter(
    prefix="/ask",
    tags=["ask"],
)

@router.post(
    "/",
    response_class=ORJSONResponse,
    status_code=status.HTTP_200_OK,
    response_model=Answer,
)
async def post(
    payload: Question,
):
    response = answer_question(payload.question)

    return response