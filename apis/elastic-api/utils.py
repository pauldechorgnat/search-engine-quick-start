from elasticsearch import Elasticsearch, helpers, BadRequestError
import os
import time


def get_env_variable(env_variable_name: str) -> str:
    value = os.environ.get(env_variable_name)
    if value is None:
        raise EnvironmentError(f"{env_variable_name} is not set")
    return value


def parse_input(query: str):
    return query


def get_document_by_id(
    elastic_search_client: Elasticsearch,
    index_name: str,
    document_id: str,
) -> dict | None:
    try:
        res = elastic_search_client.get(
            index=index_name,
            id=document_id,
        )
        return res["_source"]
    except Exception:
        return None


def search_documents(
    elastic_search_client: Elasticsearch,
    index_name: str,
    text_query: str,
    fields: list[str],
    page_size: int = 10,
    page_number: int = 0,
) -> tuple[list[dict], int]:
    query = {
        "multi_match": {
            "query": text_query,
            "fields": fields,
        }
    }
    count = elastic_search_client.count(
        index=index_name,
        query=query,
    )
    res = elastic_search_client.search(
        index=index_name,
        query=query,
        size=page_size,
        from_=page_size * page_number,
    )
    return (
        [hit["_source"] for hit in res["hits"]["hits"]],
        count["count"],
    )


def count_documents(
    elastic_search_client: Elasticsearch,
    index_name: str,
) -> int:
    res = elastic_search_client.count(index=index_name)
    return res["count"]


def create_index(
    elastic_search_client: Elasticsearch,
    index_name: str,
) -> None:
    try:
        elastic_search_client.indices.create(
            index=index_name,
        )
    except BadRequestError:
        pass


def insert_documents(
    elastic_search_client: Elasticsearch,
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
        client=elastic_search_client,
        actions=actions,
    )


def delete_all_documents(
    elastic_search_client: Elasticsearch,
    index_name: str,
) -> None:
    elastic_search_client.delete_by_query(
        index=index_name,
        body={
            "query": {
                "match_all": {},
            }
        },
    )


def wait_for_elasticsearch(
    elastic_search_client: Elasticsearch,
    retries: int = 30,
):
    for i in range(retries):
        try:
            health = elastic_search_client.cluster.health(
                wait_for_status="green",
            )
            status = health["status"]
            if status == "green":
                return True
            else:
                pass
        except Exception:
            pass
        time.sleep(5)
    return False
