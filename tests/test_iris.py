import re
import test_iris_settings
import test_iris_settings_bypass
import pytest
from moto import mock_sns, mock_sqs
from iris.iris_client import IrisClient, IrisListener
import boto3


@pytest.fixture
def iris_infrastructure():

    mock_sqs().start()
    mock_sns().start()
    sns_res = boto3.resource('sns', region_name=test_iris_settings.AWS_REGION)
    sqs_res = boto3.resource('sqs', region_name=test_iris_settings.AWS_REGION)
    topic = sns_res.create_topic(Name=test_iris_settings.IRIS_SNS_TOPIC)
    queue = sqs_res.create_queue(QueueName=test_iris_settings.IRIS_SQS_APP_QUEUE)
    queue_arn = queue.attributes['QueueArn']
    topic_arn = topic.arn
    sns_res.meta.client.subscribe(
        TopicArn=topic_arn,
        Protocol='sqs',
        Endpoint=queue_arn
    )

    yield {
        'sns_res': sns_res,
        'sqs_res': sqs_res,
        'topic': topic,
        'queue': queue,
        'topic_arn': topic_arn,
        'queue_arn': queue_arn
    }
    mock_sns().stop()
    mock_sqs().stop()


def test_sending_receiving(iris_infrastructure):

    # run test
    client = IrisClient(settings=test_iris_settings)
    client.send_iris_message({'prop': 'value'})

    # check result
    queue = iris_infrastructure['queue']
    queue.reload()
    messages = queue.receive_messages()
    assert len(messages) == 1


def test_sending_bypass(iris_infrastructure):

    # run test
    client = IrisClient(settings=test_iris_settings_bypass)
    client.send_iris_message({'prop': 'value'})

    # check result
    queue = iris_infrastructure['queue']
    queue.reload()
    messages = queue.receive_messages()
    assert len(messages) == 0


@pytest.mark.timeout(10)
@pytest.mark.usefixtures('iris_infrastructure')
def test_receiving():

    # run test
    prop = 'test_property'
    prop_value = 'test_property_value'

    # send a message to topic
    client = IrisClient(settings=test_iris_settings)
    client.send_iris_message({prop: prop_value})

    # start listener and setup container
    listener = IrisListener(settings=test_iris_settings)
    container = ListenerContainer(listener, max_messages=1)

    # will run until container stops it or test times out
    listener.run(container.callback)
    message = container.messages[0]
    assert message[prop] == prop_value


class ListenerContainer:

    def __init__(self, listener, max_messages=1):
        self.listener = listener
        self.messages = []
        self.max_messages = max_messages

    def callback(self, message):
        self.messages.append(message)
        if len(self.messages) == self.max_messages:
            self.listener.stop = True


def is_uuid4(potential_match):
    return bool(re.match(
                    (
                            '[a-f0-9]{8}-' +
                            '[a-f0-9]{4}-' +
                            '4' + '[a-f0-9]{3}-' +
                            '[89ab][a-f0-9]{3}-' +
                            '[a-f0-9]{12}$'
                    ),
                    potential_match,
                    re.IGNORECASE
                    ))


def test_session_id():

    client = IrisClient(settings=test_iris_settings)
    session_id = client.get_new_session_id()
    assert is_uuid4(session_id)
