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

## Docker

build the image locally

```
docker build -t pastebin-backend .
```

run the container

```
docker run -p 8000:8000 pastebin-backend
```

FastAPI app is available on: [http://localhost:8000](http://localhost:8000)

## API - locally

use built-in swagger

```
pipenv run uvicorn app.main:app --reload
```

<http://127.0.0.1:8000/docs>
