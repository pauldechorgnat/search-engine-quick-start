import os
import json
import random

from models import Document


def refresh_data():
    """This function reads documents.json, shuffles it and rewrites it."""
    with open(
        os.path.join(os.path.dirname(__file__), "documents.json"),
        "r",
        encoding="utf-8",
    ) as file:
        documents = json.load(file)

    random.shuffle(documents)

    documents = [Document(**d).model_dump(mode="json") for d in documents]

    with open(
        os.path.join(os.path.dirname(__file__), "documents.json"),
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            documents,
            file,
            indent=4,
        )


if __name__ == "__main__":
    refresh_data()
