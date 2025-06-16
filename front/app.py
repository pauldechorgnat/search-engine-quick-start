from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from utils import (
    parse_search_query,
    query_get_document,
    query_get_search,
)
from models import DocumentNotFoundException
from config import client, PAGE_SIZE

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(
    DocumentNotFoundException,
)
def get_document_not_found_exception(request: Request, exc: DocumentNotFoundException):
    return templates.TemplateResponse(
        request=request,
        name="404.html",
        status_code=404,
        context={
            "document_id": exc.document_id,
        },
    )


@app.get("/")
def render_search(
    request: Request,
    page_number: int | None = None,
    search_query: str | None = None,
):
    if page_number is None:
        page_number = 0

    if search_query is not None:
        query_string, query_parameters = parse_search_query(search_query)

        response = query_get_search(
            client=client,
            query=query_string,
            query_parameters=query_parameters,
            page_size=PAGE_SIZE,
        )

        total = response.n_results
        documents = response.results

        n_pages = total // PAGE_SIZE
        if total % PAGE_SIZE > 0:
            n_pages += 1

    else:
        documents = []
        query_parameters = {}
        total = None
        query_string = None
        n_pages = None

    min_page = max(int(page_number) - 3, 0)
    max_page = min(n_pages, int(page_number) + 4) if n_pages else 0

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "documents": documents,
            "parameters": query_parameters,
            "total": total,
            "query_string": query_string,
            "n_pages": n_pages,
            "page_number": page_number,
            "min_page": min_page,
            "max_page": max_page,
        },
    )


@app.get(
    "/document/{document_id}",
    response_class=HTMLResponse,
)
def get_document(
    request: Request,
    document_id: str,
):
    document = query_get_document(
        client=client,
        document_id=document_id,
    )

    return templates.TemplateResponse(
        request=request,
        name="document.html",
        context={"document": document},
    )


# if __name__ == "__main__":
#     import uvicorn
#     from argparse import ArgumentParser

#     argument_parser = ArgumentParser(
#         description="Search engine application",
#     )
#     argument_parser.add_argument(
#         "--host",
#         help="Application host",
#         default="0.0.0.0",
#     )

#     argument_parser.add_argument(
#         "-p",
#         "--port",
#         help="Application port",
#         default=2022,
#         type=int,
#     )
#     argument_parser.add_argument(
#         "-d",
#         "--debug",
#         action="store_true",
#         help="Debug mode",
#     )

#     arguments = argument_parser.parse_args()

#     uvicorn.run(
#         "main:app",
#         host=arguments.host,
#         port=arguments.port,
#         # debug=arguments.debug,
#     )
