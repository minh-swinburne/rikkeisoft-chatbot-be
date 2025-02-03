import boto3

def get_client(service_name):
    return boto3.client(service_name)