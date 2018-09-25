import os
IRIS_BYPASS = False
AWS_REGION = os.environ.get('IRIS_AWS_REGION')  # "us-west-1"
IRIS_SNS_TOPIC = os.environ.get('IRIS_TOPIC')  # "iris-test-topic"
IRIS_SQS_APP_QUEUE = os.environ.get('IRIS_QUEUE')  # "iris-presley-queue"
IRIS_POLL_INTERVAL = 20
