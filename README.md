[![PyTest](https://github.com/socraticDevBlog/pastebin/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/socraticDevBlog/pastebin/actions/workflows/pytest.yml)
# poor man cloud-native pastebin

this project is about using AWS Free tier resources to host yourown pastebin

> A pastebin or text storage site is a type of online content-hosting service
> where users can store plain text (e.g. source code snippets for code review
> via Internet Relay Chat (IRC))

## Authors

- [@socraticDevBlog](https://www.github.com/socraticDevBlog)

## Run Locally

Clone the project

```bash
  git clone git@github.com:socraticDevBlog/pastebin.git
```

Go to the project directory

```bash
  cd pastebin
```

Install dependencies

```bash
pipenv install --deploy --dev
```

Start DynamoDB local instance

```bash
 cd local

 docker compose up
```

## Running Tests

To run tests, run the following command

```bash
pipenv run test -v
```

## Roadmap

- [x] implement a DynamoDB CRUD client

- [x] safe-guard CI by automated unit tests suite (GitHub Action)

- [ ] implement CI 'better practices' automated safe-guards

- [ ] develop a lambda that will Create and Read pastes

- [ ] implement an API Gateway that exposes Lamba's functions via http endpoints

- [ ] deploy required infrastructure using Terraform in AWS

## Tech Stack

**database:** aws DynamoDB

**computing:** aws Lambda, python, boto3

**publicly available endpoint:** aws API Gateway

**CI/CD**: GitHub, GitHub Actions, pyenv, pytest

### local dev environment

- Docker
- DynamoDB local
- SAM (Lambda), awscli
- localStack (API Gateway)
