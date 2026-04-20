import os.path
import boto3
import os
import requests
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

def read_file(filepath: str) -> str:
    """read file content by filepath"""

    if not os.path.exists(filepath):
        return f"Error: file {filepath} not exist"
    with open(filepath, "r") as f:
        return f.read()

def read_s3_file(bucket: str, s3key: str) -> str:
    """read file content by s3 bucket and key"""
    try:
        obj = s3_client.get_object(Bucket=bucket, Key=s3key)
        return obj["Body"].read().decode("utf-8")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code in {"NoSuchKey", "404", "NotFound"}:
            return f"s3 file s3://{bucket}/{s3key} not found"
        raise

def write_file(filepath: str, content: str) -> str:
    """write content to file by filepath"""

    with open(filepath, "w") as f:
        f.write(content)

    return f"wrote file {filepath}"

def write_s3_file(bucket: str, s3key: str, content: str) -> str:
    """write content to s3 with bucket and key"""

    s3_client.put_object(Bucket=bucket, Key=s3key, Body=content)
    return f"wrote file s3://{bucket}/{s3key}"

def web_fetch(url: str) -> str:
    """fetch web HTML content by url"""

    return requests.get(url).text

if __name__ == '__main__':
    print(web_fetch("https://yanbin.blog"))