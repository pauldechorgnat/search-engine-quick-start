FROM python:3.13-slim

WORKDIR /api

COPY mock-api.requirements.txt .

RUN pip install -r mock-api.requirements.txt

COPY  api.py  models.py utils.py refresh_data.py documents.json /api/

CMD [ "python", "-m", "uvicorn", "api:api", "--host", "0.0.0.0", "--port", "8000" ]