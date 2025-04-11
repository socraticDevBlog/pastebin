FROM python:3.13.3-slim

WORKDIR /app

COPY Pipfile Pipfile.lock ./
COPY app ./app

RUN pip install --no-cache-dir pipenv

ENV PIPENV_VENV_IN_PROJECT=1

RUN pipenv install --dev

EXPOSE 8000

CMD ["pipenv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]