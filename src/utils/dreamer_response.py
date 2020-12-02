import json

from rest_framework import status
from rest_framework.response import Response


class DreamerResponse:
    def __init__(self, data, message=None, code=status.HTTP_200_OK, headers=None, message_code='ok'):
        self.message = message
        self.message_code = message_code
        self.code = code
        self.data = data
        self.headers = headers

    def toJSON(self):
        return json.dumps(self.__dict__)

    def toJSONResponse(self):
        res = self.__dict__
        headers = res.pop('headers')
        code = res.pop('code')
        return Response(res, status=code, headers=headers)
