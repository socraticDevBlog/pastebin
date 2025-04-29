FROM python:3.13.3-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install --no-cache-dir pipenv && pipenv install --dev

COPY app ./app

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]