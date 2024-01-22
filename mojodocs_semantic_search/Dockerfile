FROM python:3.11

WORKDIR /app

COPY requirements.txt /app
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["gunicorn", "mojodocs_semantic_search.wsgi:application", "--bind", "0.0.0.0:8000"]
