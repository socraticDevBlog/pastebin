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

### Start DynamoDB local instance

```bash
 cd local

 docker compose up
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
pipenv run sam build && pipenv run sam local invoke -e local/events/post.json

# > Invoking app.lambda_handler (python3.9)
# Local image is up-to-date
# Using local image: public.ecr.aws/lambda/python:3.9-rapid-x86_64.

# Mounting /Users/me/git/pastebin/.aws-sam/build/PastebinFunction as /var/task:ro,delegated, inside runtime container
# START RequestId: 378e46ab-dd9b-4a31-bec7-1cc1b4a06ae8 Version: $LATEST
# END RequestId: 378e46ab-dd9b-4a31-bec7-1cc1b4a06ae8
# REPORT RequestId: 378e46ab-dd9b-4a31-bec7-1cc1b4a06ae8  Init Duration: 1.52 ms  Duration: 1021.66 ms    Billed Duration: 1022 ms        Memory Size: 128 MB     Max Memory Used: 128 MB
```

### run API Gateway locally

sam CLI will detect the API Gateway and its available methods automatically
(GET, POST, etc.)

developer will use Postman app or VS Code Thunder Client to issue http request
toward `localhost:3000/paste` endpoint


```bash
pipenv run sam local start-api

# Initializing the lambda functions containers.                                                                                                                                                         
# Local image is up-to-date                                                                                                                                                                             
# Using local image: public.ecr.aws/lambda/python:3.9-rapid-x86_64.                                                                                                                                     
                                                                                                                                                                                                      
# Mounting /Users/user/Documents/git/pastebin/.aws-sam/build/PastebinFunction as /var/task:ro,delegated, inside runtime container                                                                
# Containers Initialization is done.                                                                                                                                                                    
# Mounting PastebinFunction at http://127.0.0.1:3000/paste [GET]                                                                                                                                        
# You can now browse to the above endpoints to invoke your functions. You do not need to restart/reload SAM CLI while working on your functions, changes will be reflected instantly/automatically. If  
# you used sam build before running local commands, you will need to re-run sam build for the changes to be picked up. You only need to restart SAM CLI if you update your AWS SAM template             
# 2023-08-09 17:19:04 WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
#  * Running on http://127.0.0.1:3000
# 2023-08-09 17:19:04 Press CTRL+C to quit
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
