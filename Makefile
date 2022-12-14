include .env

setup:
	pipenv install
	pulumi login --local

create-stack:
	cd examples/$(example) && pulumi stack init $(example)
	cd examples/$(example) && pulumi config set gcp:project ${PROJECT_ID}
	cd examples/$(example) && pulumi config set gcp:region EU

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
