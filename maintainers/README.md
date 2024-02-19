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