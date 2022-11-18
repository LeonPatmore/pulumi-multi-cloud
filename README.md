# Pulumi Multi Cloud

## Resources

- https://www.pulumi.com/docs/intro/concepts/how-pulumi-works/
- https://github.com/pulumi/examples/blob/master/aws-py-s3-folder/__main__.py

### Existing Solutions

#### Serverless

- https://github.com/serverless/multicloud
- https://github.com/mikestaub/serverless-express
- https://github.com/jasonumiker/serverless-multicloud-example

## Requirements

- AWS CLI
- GCP CLI
- Pulumi CLI
- pipenv

## Local Testing

Ensure you create a `.env` file with the following contents:

```
export PROJECT_ID=<gcp project id>
export PULUMI_CONFIG_PASSPHRASE=<pulumi config password>
```
