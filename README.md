# Pulumi Multi Cloud

## Resources

- https://www.pulumi.com/docs/intro/concepts/how-pulumi-works/
- https://github.com/pulumi/examples

### Existing Solutions

#### Serverless

- https://github.com/serverless/multicloud
- https://github.com/mikestaub/serverless-express
- https://github.com/jasonumiker/serverless-multicloud-example

## Requirements

- AWS CLI
- GCP CLI
- Azure CLI
- Pulumi CLI
- pipenv

## Local Testing

Ensure you create a `.env` file with the following contents:

```
export PROJECT_ID=<gcp project id>
export PULUMI_CONFIG_PASSPHRASE=<pulumi config password>
```

## Running Examples

In the following commands, replace `<example_dir>` with one of the following:

- function
- storage

List the stacks:

`make list-stacks example=<example_dir`

To run an example:

`make update-stack example=<example_dir>`
