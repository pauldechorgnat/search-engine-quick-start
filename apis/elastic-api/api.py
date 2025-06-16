from fastapi import FastAPI
from fastapi.exceptions import HTTPException

from models import Document, SearchResponse, StatusOKResponse
from utils import get_document_by_id, search_documents, get_env_variable
from elasticsearch import Elasticsearch

ELASTICSEARCH_HOSTS = get_env_variable("ELASTICSEARCH_HOSTS")
ELASTIC_INDEX_NAME = get_env_variable("ELASTIC_INDEX_NAME")
elasticsearch_client = Elasticsearch(hosts=ELASTICSEARCH_HOSTS)

api = FastAPI()


@api.get(
    "/healthcheck",
    responses={
        200: {"model": StatusOKResponse, "description": "OK"},
    },
)
def get_healthcheck() -> StatusOKResponse:
    return StatusOKResponse()


@api.get(
    "/document/{document_id}",
    responses={
        200: {"model": Document, "description": "OK"},
        404: {"description": "Document not found"},
    },
)
def get_document(document_id) -> Document:
    document = get_document_by_id(
        elasticsearch_client=elasticsearch_client,
        index_name=ELASTIC_INDEX_NAME,
        document_id=document_id,
    )
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
    text_query: str | None = None,
) -> SearchResponse:
    return search_documents(
        elasticsearch_client=elasticsearch_client,
        index_name=ELASTIC_INDEX_NAME,
        page_number=page_number,
        page_size=page_size,
        text_query=text_query,
    )
