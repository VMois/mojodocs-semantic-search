FROM python:3.11

WORKDIR /app

RUN pip install --upgrade pip

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "mojodocs_semantic_search.wsgi:application", "--bind", "0.0.0.0:8000"]
