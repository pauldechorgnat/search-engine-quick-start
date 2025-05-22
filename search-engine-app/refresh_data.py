import datetime

from elasticsearch import Elasticsearch

from utils import (
    wait_for_elasticsearch,
    create_index,
    count_documents,
    delete_all_documents,
    insert_documents,
)


def read_data_to_insert(
    *args,
    **kwargs,
) -> list[dict]:
    from lorem_text import lorem
    import random

    data = [
        {
            "text": lorem.paragraphs(random.randint(4, 10)),
            "name": lorem.words(random.randint(4, 10)),
            "date": datetime.date(year=2020, month=1, day=1) + datetime.timedelta(days=random.randint(1, 365 * 4)),
            "id": str(i),
        }
        for i in range(50)
    ]

    return data


def format_data(data: dict) -> dict:
    return data


def refresh_data(
    new_data: list[dict],
    index_name: str,
    elastic_search_client: Elasticsearch,
    id_field: str = "id",
    replace_old_data: bool = True,
):
    if not wait_for_elasticsearch(
        elastic_search_client=elastic_search_client,
    ):
        raise ValueError("ElasticSearch cannot be reached")

    create_index(
        elastic_search_client=elastic_search_client,
        index_name=index_name,
    )

    n_documents = count_documents(
        elastic_search_client=elastic_search_client,
        index_name=index_name,
    )

    documents = [format_data(d) for d in new_data]

    if replace_old_data:
        delete_all_documents(
            elastic_search_client=elastic_search_client,
            index_name=index_name,
        )
    insert_documents(
        elastic_search_client=elastic_search_client,
        index_name=index_name,
        docs=documents,
        id_field=id_field,
    )
    n_documents = count_documents(
        elastic_search_client=elastic_search_client,
        index_name=index_name,
    )
    print(f"{n_documents} documents in '{index_name}'")


if __name__ == "__main__":
    from dotenv import load_dotenv
    from utils import get_env_variable

    load_dotenv()

    ELASTICSEARCH_HOSTS = get_env_variable("ELASTICSEARCH_HOSTS")
    ELASTIC_INDEX_NAME = get_env_variable("ELASTIC_INDEX_NAME")

    es = Elasticsearch(ELASTICSEARCH_HOSTS)

    refresh_data(
        new_data=read_data_to_insert(...),
        index_name=ELASTIC_INDEX_NAME,
        elastic_search_client=es,
    )
