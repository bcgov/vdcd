from rest_framework.viewsets import GenericViewSet
from api.authentication import CustomTokenAuthentication
from api.models import DecodedVinRecord
from api.services.decoded_vin_record import get_decoded_vins
from rest_framework.decorators import action
from rest_framework.response import Response


class DecodedVinRecordViewset(GenericViewSet):
    authentication_classes = [CustomTokenAuthentication]

    queryset = DecodedVinRecord.objects.all()

    @action(detail=False, methods=["post"])
    def get_decoded_vins(self, request):
        vins = request.data.get("vins")
        decoded_vins = get_decoded_vins(vins)
        return Response(decoded_vins)
