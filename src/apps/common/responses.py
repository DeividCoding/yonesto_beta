from rest_framework.response import Response
from rest_framework.status import is_client_error


class EnvelopeResponse(Response):
    def __init__(
        self, data=None, message=None, links=None, count=None, *args, **kwargs
    ):
        success = True
        message_data = None
        if is_client_error(kwargs.get("status", 200)):
            message_data_links = {"links": links, "count": count}
            message_data = data
            success = False
        else:
            message_data_links = {"links": links, "count": count}
            message_data = data

        result = {
            "Success": success,
            **message_data_links,
            "Message": message,
            "Data": message_data,
        }
        super(EnvelopeResponse, self).__init__(data=result, *args, **kwargs)
