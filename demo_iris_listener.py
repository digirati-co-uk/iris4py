import iris_client
import json


def print_message(message):

    print(json.dumps(message))


listener = iris_client.IrisListener()
listener.run(print_message, None)
