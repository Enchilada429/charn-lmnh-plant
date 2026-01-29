"""This script provides downloadable links to objects in the S3 buckets."""

from os import environ as ENV, _Environ

from dotenv import load_dotenv
from re import match
from boto3 import client
from mypy_boto3_s3.client import S3Client


def get_s3_client(config: _Environ) -> client:
    """Returns a live S3 client."""

    return client(
        "s3",
        aws_access_key_id=config["AWS_ACCESS_KEY"],
        aws_secret_access_key=config["AWS_SECRET_KEY"]
    )


def get_object_list(s3_client: S3Client, bucket_name: str, regex: str=r".*\.csv$") -> list[str]:
    """Returns a list of objects inside the S3 bucket.
    Optional regex parameter to specify object names wanted."""

    objects = s3_client.list_objects(Bucket=bucket_name)["Contents"]

    return [object["Key"] for object in objects if match(regex, object["Key"])]


def generate_object_url(bucket_name: str, object_name: str) -> str:
    """Returns a download link to object in S3 bucket."""

    return f"https://{bucket_name}.s3.{ENV["AWS_REGION"]}.amazonaws.com/{object_name}"


def get_all_object_urls(s3_client: S3Client, bucket_name: str) -> dict:
    """Returns a dict of all object names and download links in the bucket."""

    object_list = get_object_list(s3_client, bucket_name)

    return {object_name: generate_object_url(bucket_name, object_name) for object_name in object_list}


if __name__ == "__main__":

    load_dotenv()

    s3 = get_s3_client(ENV)

    print(get_all_object_urls(s3, ENV["S3_BUCKET"]))
