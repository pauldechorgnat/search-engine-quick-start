import os
from httpx import Client, HTTPError
from models import Document, SearchResponse, DocumentNotFoundException


def get_env_variable(
    env_variable_name: str,
    default: str | None = None,
) -> str:
    value = os.environ.get(env_variable_name, default=default)
    if value is None:
        raise EnvironmentError(f"{env_variable_name} is not set")
    return value


def parse_search_query(query: str) -> tuple[str, dict]:
    return query, {}


def query_get_document(
    client: Client,
    document_id: str,
) -> Document:
    print("LOOOOL")
    response = client.get(url=f"/document/{document_id}")
    print("YOOOOOO")
    try:
        response.raise_for_status()
    except HTTPError as exc:
        if response.status_code == 404:
            raise DocumentNotFoundException(document_id=document_id) from exc
        raise exc
    return Document(**response.json())


def query_get_search(
    client: Client,
    query: str,
    query_parameters: dict = {},
    page_size: int = 5,
    page_number: int = 0,
) -> SearchResponse:
    response = client.get(
        url="/search",
        params={
            "query": query,
            **query_parameters,
        },
    )
    response.raise_for_status()

    return SearchResponse(**response.json())
