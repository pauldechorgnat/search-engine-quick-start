from flask import Flask, render_template, request, abort
from elasticsearch import Elasticsearch
from utils import (
    parse_input,
    get_document_by_id,
    search_documents,
    get_env_variable,
)
from dotenv import load_dotenv

load_dotenv()

ELASTICSEARCH_HOSTS = get_env_variable("ELASTICSEARCH_HOSTS")
ELASTIC_INDEX_NAME = get_env_variable("ELASTIC_INDEX_NAME")

elastic_search_client = Elasticsearch(ELASTICSEARCH_HOSTS)

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.get("/")
def render_search():
    parameters = {}
    if "page-number" in request.args:
        page_number: int = int(request.args["page-number"])
    else:
        page_number = 0
    if "search-query" in request.args:
        query_string = request.args["search-query"]
        # parameters = parse_input(query_string)
        query_string = parse_input(query_string)
        documents, total = search_documents(
            elastic_search_client=elastic_search_client,
            text_query=query_string,
            page_number=page_number,
            index_name=ELASTIC_INDEX_NAME,
            fields=["text"],
        )

        n_pages = total // 25
        if total % 25 > 0:
            n_pages += 1

    else:
        documents = []
        parameters = {}
        total = None
        query_string = None
        n_pages = None

    min_page = max(int(page_number) - 3, 0)
    max_page = min(n_pages, int(page_number) + 4) if n_pages else 0

    return render_template(
        "index.html",
        documents=documents,
        parameters=parameters,
        total=total,
        query_string=query_string,
        n_pages=n_pages,
        page_number=int(page_number),
        min_page=min_page,
        max_page=max_page,
    )


@app.get("/document/<document_id>")
def get_document_page(document_id: str):
    document = get_document_by_id(
        elastic_search_client=elastic_search_client,
        index_name=ELASTIC_INDEX_NAME,
        document_id=document_id,
    )
    if document is None:
        abort(404)
    return render_template(
        "document.html",
        document=document,
    )


if __name__ == "__main__":
    from argparse import ArgumentParser

    argument_parser = ArgumentParser(
        description="Search engine application",
    )
    argument_parser.add_argument(
        "--host",
        help="Application host",
        default="0.0.0.0",
    )

    argument_parser.add_argument(
        "-p",
        "--port",
        help="Application port",
        default=2022,
        type=int,
    )
    argument_parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Debug mode",
    )

    arguments = argument_parser.parse_args()

    app.run(
        host=arguments.host,
        port=arguments.port,
        debug=arguments.debug,
    )
