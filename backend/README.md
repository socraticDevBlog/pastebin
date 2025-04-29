![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)

# pastebin.backend

## dependencies management

| tool                                                    | why                   |
| ------------------------------------------------------- | --------------------- |
| [pyenv](https://github.com/pyenv/pyenv)                 | manage python version |
| [pipenv](https://docs.pipenv.org/en/latest/basics.html) | manage dependencies   |

### setup pipenv

when working on the fastapi backend, you want to be using the
`/backend/Pipfile` with `pipenv`

avoid trouble by setting up these two environment variable before using `pipenv`

```
# tell pipenv to use the /backend/Pipfile
export PIPENV_PIPFILE=$(pwd)/Pipfile

```

## run api in dev mode

```
pipenv run fastapi dev
```

## Docker compose

build the app image locally

```
docker build -t pastebin-backend .
```

have a `.env` file at the root of the `/backend` directory and fill it out with
these values

```ini
DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=mydeb
DB_SCHEMA=myschema
DB_HOST=db # must match docker-compose file service name
```

run the app alongside a Postgresql database on your local machine

```bash
docker compose up --build
```

to reset your docker environment

```bash
docker compose down --volumes
```

FastAPI app swagger is available on: [http://localhost:8010/docs](http://localhost:8010/docs)

## API - locally

use built-in swagger

```
pipenv run uvicorn app.main:app --reload
```

<http://127.0.0.1:8000/docs>

## unit tests

```bash
pipenv run pytest
```