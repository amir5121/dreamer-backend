import json

from rest_framework import status
from rest_framework.response import Response


class DreamerResponse:
    def __init__(self, data, message='ok', code=status.HTTP_200_OK, headers=None):
        self.message = message
        self.code = code
        self.data = data
        self.headers = headers

    def toJSON(self):
        return json.dumps(self.__dict__)

    def toJSONResponse(self):
        res = self.__dict__
        headers = res.pop('headers')
        return Response(res, status=self.code, headers=headers)
