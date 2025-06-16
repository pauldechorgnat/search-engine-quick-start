from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from models import Document, SearchResponse
from utils import get_document_by_id, search_documents

api = FastAPI()


@api.get("/healthcheck")
def get_healthcheck():
    return {"status": "ok"}


@api.get(
    "/document/{document_id}",
    responses={
        200: {"model": Document, "description": "OK"},
        404: {"description": "Document not found"},
    },
)
def get_document(document_id) -> Document:
    document = get_document_by_id(document_id=document_id)
    if document is None:
        raise HTTPException(
            status_code=404,
            detail=f"Document with id '{document_id}' not found",
        )
    return document


@api.get(
    "/search",
    responses={
        200: {"model": SearchResponse, "description": "OK"},
    },
)
def get_search(
    page_number: int = 0,
    page_size: int = 5,
    query: str | None = None,
) -> SearchResponse:
    return search_documents(
        page_number=page_number,
        page_size=page_size,
        query=query,
    )
