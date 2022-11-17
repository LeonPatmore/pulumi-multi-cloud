
setup:
	pulumi login --local

create-stack:
	pulumi stack init example

update-stack:
	pipenv run pulumi up

cleanup:
	pulumi destroy
