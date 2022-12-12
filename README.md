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

## Setting up Pulumi

The easiest way to set up Pulumi is to use a local storage:

`pulumi login --local`

Or use `make setup`.

## Running Examples

In the following commands, replace `<example_dir>` with one of the following:

- function
- storage

Setup the example:

`make create-stack example=<example_dir>`

List the stacks:

`make list-stacks example=<example_dir>`

Refresh a stack:

`make refresh example=<example_dir>`

To run an example:

`make update-stack example=<example_dir>`

## Known Issues

### GCP Functions

- Uploading function code with embedded folders/modules with Windows will not work for GCP functions. This is because windows uses
forwarded slashes instead of backslashes.
