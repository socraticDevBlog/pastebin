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

### Run Lambda locally

Using SAM (Serverless Application Model) CLI, you can easily execute the lambda
locally

We are using only one (1) lambda entrypoint to cover all http requests since
our use case is pretty simple.

Lambda code is located at `src/app.py`

Stubbed lambda _event_ input arguments are located at `local/events/`. There is
one file per http verb.

#### simulate a POST request locally

```bash
pipenv run sam build

pipenv run sam local invoke -e local/events/post.json

# > Invoking app.lambda_handler (python3.9)
# Local image is up-to-date
# Using local image: public.ecr.aws/lambda/python:3.9-rapid-x86_64.

# Mounting /Users/me/git/pastebin/.aws-sam/build/PastebinFunction as /var/task:ro,delegated, inside runtime container
# START RequestId: 378e46ab-dd9b-4a31-bec7-1cc1b4a06ae8 Version: $LATEST
# END RequestId: 378e46ab-dd9b-4a31-bec7-1cc1b4a06ae8
# REPORT RequestId: 378e46ab-dd9b-4a31-bec7-1cc1b4a06ae8  Init Duration: 1.52 ms  Duration: 1021.66 ms    Billed Duration: 1022 ms        Memory Size: 128 MB     Max Memory Used: 128 MB
```

### Start DynamoDB local instance

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

**dependencies management** pipenv

**database:** aws DynamoDB

**computing:** aws Lambda, python, boto3

**publicly available endpoint:** aws API Gateway

**CI/CD**: GitHub, GitHub Actions, pyenv, pytest

### local dev environment

- Docker
- DynamoDB local
- SAM (Lambda), awscli
