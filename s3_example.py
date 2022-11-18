from pulumi_aws import s3
from pulumi_gcp import storage

s3.Bucket('leon-patmore-example')
storage.Bucket("leon-patmore-example", location="EU")
