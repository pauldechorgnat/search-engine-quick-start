from pydantic import BaseModel, Field
from uuid import uuid4
import datetime
import random


def generate_random_date() -> datetime.date:
    return datetime.date(year=2020, month=1, day=1) + datetime.timedelta(days=random.randint(0, 5 * 365))


class SearchResult(BaseModel):
    id: str
    date: datetime.date
    title: str


class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    date: datetime.date = Field(default_factory=generate_random_date)
    title: str
    text: str

    def to_search_result(self) -> SearchResult:
        return SearchResult(
            id=self.id,
            date=self.date,
            title=self.title,
        )


class SearchResponse(BaseModel):
    n_results: int
    results: list[SearchResult]


class DocumentNotFoundException(Exception):
    pass
