from elasticsearch import Elasticsearch

from models import Document
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
) -> list[Document]:
    from lorem_text import lorem
    import random

    data = [
        Document(
            text=lorem.paragraphs(random.randint(4, 10)),
            title=lorem.words(random.randint(4, 10)),
        )
        for i in range(50)
    ]

    return data


def format_data(data: Document) -> dict:
    return data.model_dump(mode="json")


def refresh_data(
    new_data: list[Document],
    index_name: str,
    elasticsearch_client: Elasticsearch,
    id_field: str = "id",
    replace_old_data: bool = True,
):
    print("YOOOOOO")
    if not wait_for_elasticsearch(
        elasticsearch_client=elasticsearch_client,
    ):
        raise ValueError("ElasticSearch cannot be reached")

    create_index(
        elasticsearch_client=elasticsearch_client,
        index_name=index_name,
    )

    n_documents = count_documents(
        elasticsearch_client=elasticsearch_client,
        index_name=index_name,
    )

    documents = [format_data(d) for d in new_data]

    if replace_old_data:
        delete_all_documents(
            elasticsearch_client=elasticsearch_client,
            index_name=index_name,
        )
    insert_documents(
        elasticsearch_client=elasticsearch_client,
        index_name=index_name,
        docs=documents,
        id_field=id_field,
    )
    n_documents = count_documents(
        elasticsearch_client=elasticsearch_client,
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
        elasticsearch_client=es,
    )
    print("Data has been inserted")
