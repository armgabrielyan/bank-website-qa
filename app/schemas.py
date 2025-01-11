from pydantic import BaseModel

class Question(BaseModel):
    question: str

class Source(BaseModel):
    id: str
    title: str
    url: str

class Answer(BaseModel):
    answer: str
    sources: list[Source]
