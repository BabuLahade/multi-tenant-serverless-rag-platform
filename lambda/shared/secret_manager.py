import boto3

AWS_REGION = "ap-south-1"


def get_secret(secret_name):

    client = boto3.client(
        "secretsmanager",
        region_name=AWS_REGION
    )

    response = client.get_secret_value(
        SecretId=secret_name
    )

    return response["SecretString"]