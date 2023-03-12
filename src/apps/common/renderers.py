from rest_framework import renderers


class MessageRenderer(renderers.JSONRenderer):
    media_type = "application/json"
    format = "message"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # import pudb; pudb.set_trace()

        is_failed = renderer_context["response"].exception
        message = None
        if is_failed:
            message = data.pop("detail", None)
            if message is None:
                message = data
                data = None
        if data == {}:
            data = None

        response = {"Success": not (is_failed), "Message": message, "Data": data}
        return super().render(response, accepted_media_type, renderer_context)
