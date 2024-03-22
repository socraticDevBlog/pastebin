# maintainers README

## stack

### GitHub Actions

### AWS OIDC

Connecting GitHub Actions to AWS to perform Terraform provisionning is best
with OIDC provider.

This is setup within your AWS account (IAM/Identity Provider) where a link is
explicitely set between an IAM role and this specific GitHub project

[ Deploy to AWS with Terraform within a GitHub Action ](https://www.youtube.com/watch?v=GowFk_5Rx_I)

### AWS IAM role and policies

get inspiration from `policies.json` to figure out what permissions need to be
assigned to the Role used by OIDC/GitHub Actions

## locally

running Terraform locally is also possible to speed up the feedback loop:

(required: have `aws cli`, `tfswitch`, and `pipenv` installed on your local machine)

- get an aws dev-user from us and create an Access key on AWS web console
-  configure your aws cli with your these credentials

```bash
# answer interactive prompt

aws config
```

- run homemade [assume-role.sh](assume-role.sh) script to be able to perform actions on aws

```bash
source assume-role.sh
```
