from iris import iris_client

iris = iris_client.IrisClient()

message = {
    'message_type': 'Event_Has_Happened',
    'event_specific_field': 'http://a.link.to.entity/',
    'session': iris.get_new_session_id()
}

iris.send_iris_message(message)
