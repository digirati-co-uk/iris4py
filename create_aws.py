import iris_settings as settings
import boto3
from botocore.exceptions import ClientError

try:
    sns_client = boto3.client('sns', settings.AWS_REGION)
    response = sns_client.create_topic(
        Name=settings.IRIS_SNS_TOPIC
    )

    print(response)
    print("\n\n\n")
    sqs_client = boto3.client('sqs', settings.AWS_REGION)
    response = sqs_client.create_queue(
        QueueName=settings.IRIS_SQS_APP_QUEUE
    )

    print(response)

except ClientError as e:
    print("Error creating resources:")
    print(e.response['Error']['Code'])
    print(e.response['Error']['Message'])
    exit(1)

print("Resources created")
