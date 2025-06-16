from elasticsearch import Elasticsearch, helpers, BadRequestError
import os
import time

from models import Document, SearchResponse


def get_env_variable(env_variable_name: str) -> str:
    value = os.environ.get(env_variable_name)
    if value is None:
        raise EnvironmentError(f"{env_variable_name} is not set")
    return value


def get_document_by_id(
    elasticsearch_client: Elasticsearch,
    index_name: str,
    document_id: str,
) -> Document | None:
    try:
        res = elasticsearch_client.get(
            index=index_name,
            id=document_id,
        )
        return Document(**res["_source"])
    except Exception:
        return None


def search_documents(
    elasticsearch_client: Elasticsearch,
    index_name: str,
    text_query: str | None,
    fields: list[str] = ["text"],
    page_size: int = 10,
    page_number: int = 0,
) -> SearchResponse:
    if text_query is None:
        text_query = "*"

    query = {
        "multi_match": {
            "query": text_query,
            "fields": fields,
        }
    }
    n_results = count_documents(
        elasticsearch_client=elasticsearch_client,
        index_name=index_name,
        text_query=text_query,
        fields=fields,
    )

    raw_results = elasticsearch_client.search(
        index=index_name,
        query=query,
        size=page_size,
        from_=page_size * page_number,
    )

    results = [hit["_source"] for hit in raw_results["hits"]["hits"]]

    return SearchResponse(
        n_results=n_results,
        results=results,
    )


def count_documents(
    elasticsearch_client: Elasticsearch,
    index_name: str,
    text_query: str | None = None,
    fields: list[str] = ["text"],
) -> int:
    if text_query is None:
        res = elasticsearch_client.count(
            index=index_name,
        )
    else:
        query = {
            "multi_match": {
                "query": text_query,
                "fields": fields,
            }
        }
        res = elasticsearch_client.count(
            index=index_name,
            query=query,
        )
    return res["count"]


def create_index(
    elasticsearch_client: Elasticsearch,
    index_name: str,
) -> None:
    try:
        elasticsearch_client.indices.create(
            index=index_name,
        )
    except BadRequestError:
        pass


def insert_documents(
    elasticsearch_client: Elasticsearch,
    index_name: str,
    docs: list[dict],
    id_field: str = "id",
) -> None:
    actions = (
        {
            "_op_type": "index",
            "_index": index_name,
            "_source": doc,
            "_id": doc.get(id_field),
        }
        for doc in docs
    )

    success, errors = helpers.bulk(
        client=elasticsearch_client,
        actions=actions,
    )


def delete_all_documents(
    elasticsearch_client: Elasticsearch,
    index_name: str,
) -> None:
    elasticsearch_client.delete_by_query(
        index=index_name,
        body={
            "query": {
                "match_all": {},
            }
        },
    )


def wait_for_elasticsearch(
    elasticsearch_client: Elasticsearch,
    retries: int = 30,
):
    for i in range(retries):
        try:
            health = elasticsearch_client.cluster.health(
                wait_for_status="green",
            )
            status = health["status"]
            if status == "green":
                return True
            else:
                pass
        except Exception:
            pass
        print(f"Trying to reach ElasticSearch {i + 1}/{retries}")
        time.sleep(5)
    return False
