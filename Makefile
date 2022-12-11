include .env

setup:
	pipenv install
	pulumi login --local
	pulumi config set gcp:project ${PROJECT_ID}
	pulumi config set gcp:region EU

create-stack:
	pulumi stack init example

update-stack:
	cd examples/$(example) &&  pipenv run pulumi up

cleanup:
	pulumi destroy

check-plugins:
	pulumi plugin ls

list-stacks:
	cd examples/$(example) && pulumi stack ls

refresh:
	cd examples/$(example) && pulumi refresh
