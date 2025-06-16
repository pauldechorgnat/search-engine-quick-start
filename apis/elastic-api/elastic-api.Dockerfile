FROM python:3.13-slim

WORKDIR /api

COPY elastic-api.requirements.txt .

RUN pip install -r elastic-api.requirements.txt

COPY  api.py  models.py utils.py refresh_data.py run-app.sh /api/

CMD [ "sh", "run-app.sh" ]