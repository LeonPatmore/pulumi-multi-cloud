include .env

setup:
	pipenv install
	pulumi login --local
	pulumi config set gcp:project ${PROJECT_ID}
	pulumi config set gcp:region EU

create-stack:
	pulumi stack init example

update-stack:
	pipenv run pulumi up

cleanup:
	pulumi destroy
