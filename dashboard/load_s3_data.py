"""Script which provides downloadable links to objects in the S3 buckets."""

from os import environ as ENV, _Environ

from dotenv import load_dotenv
from re import match
from boto3 import client
from mypy_boto3_s3.client import S3Client


S3_BUCKET_NAME = "c21-charn-archive-bucket"


def get_s3_client(config: _Environ) -> client:
    """Returns a live S3 client."""

    return client(
        "s3",
        aws_access_key_id=config["AWS_ACCESS_KEY"],
        aws_secret_access_key=config["AWS_SECRET_KEY"]
    )


def get_object_list(s3_client: S3Client, bucket_name: str, regex: str = r".") -> list[str]:
    """Gets a list of objects inside the S3 bucket.
    Optional regex parameter to specify object names wanted."""

    objects = s3_client.list_objects(Bucket=bucket_name)["Contents"]

    return [object["Key"] for object in objects if match(regex, object["Key"])]


if __name__ == "__main__":

    load_dotenv()

    s3 = get_s3_client(ENV)

    print(s3)
