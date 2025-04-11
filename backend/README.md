![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
# pastebin.backend

## setup pipenv

when working on the fastapi backend, you want to be using the
`/backend/Pipfile` with `pipenv`

avoid trouble by setting up these two environment variable before using `pipenv`

```
# tell pipenv to use the /backend/Pipfile
export PIPENV_PIPFILE=$(pwd)/Pipfile

# tell pipenv to create and use the .venv directory for virtual environment
# in this directory here
export PIPENV_VENV_IN_PROJECT=1
```

