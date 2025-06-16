FROM python:3.13-slim

WORKDIR /app

COPY front.requirements.txt .

RUN pip install -r front.requirements.txt

COPY static /app/static/
COPY templates /app/templates/

COPY  app.py config.py models.py utils.py /app/

CMD [ "python", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "2022" ]