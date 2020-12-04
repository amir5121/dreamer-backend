from rest_framework import views

from configuration.models import DreamerConfiguration
from configuration.serializers import ConfigurationsSerializer
from utils.dreamer_response import DreamerResponse


class InitialConfigView(views.APIView):

    def get(self, request, *args, **kwargs):
        context = {
            "request": request
        }
        return DreamerResponse(
            data=ConfigurationsSerializer(
                context=context,
                instance=DreamerConfiguration.objects.get(version=request.version)
            ).data
        ).toJSONResponse()
