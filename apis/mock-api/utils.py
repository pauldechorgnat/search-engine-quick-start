from models import Document, SearchResponse
import random
import json
import os
from contextlib import contextmanager


@contextmanager
def random_seed(seed):
    state = random.getstate()  # Save current state
    random.seed(seed)  # Set new seed
    try:
        yield
    finally:
        random.setstate(state)  # Restore previous state


def load_documents() -> dict[str, Document]:
    with open(
        os.path.join(os.path.dirname(__file__), "documents.json"),
        "r",
        encoding="utf-8",
    ) as file:
        documents = [Document(**d) for d in json.load(file)]
    return {document.id: document for document in documents}


def get_document_by_id(document_id: str) -> Document | None:
    documents = load_documents()
    return documents.get(document_id)


def search_documents(
    text_query: str | None = None,
    query_parameters: dict = {},
    page_number: int = 0,
    page_size: int = 5,
) -> SearchResponse:
    documents = load_documents()

    with random_seed(str(text_query) + str(query_parameters)):
        n_results = random.randint(
            a=0,
            b=100,
        )
        results = [random.choice(list(documents.values())).to_search_result() for _ in range(n_results)]

    results = results[page_number * page_size : (page_number + 1) * page_size]

    return SearchResponse(
        n_results=n_results,
        results=results,
    )
