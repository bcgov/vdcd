from rest_framework.viewsets import GenericViewSet
from api.authentication import KeycloakAuthentication
from api.models import UploadedVinRecord
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.services.minio import get_minio_put_url, get_minio_object
from api.services.uploaded_vin_record import parse_and_save
import uuid


class UploadedVinRecordViewset(GenericViewSet):
    authentication_classes = [KeycloakAuthentication]

    queryset = UploadedVinRecord.objects.all()

    @action(detail=False, methods=["GET"])
    def get_minio_put_url(self, request):
        object_name = uuid.uuid4().hex
        url = get_minio_put_url(object_name)
        return Response({"url": url, "object_name": object_name})

    @action(detail=False, methods=["POST"])
    def load_data(self, request):
        object_name = request.data.get("object_name")
        try:
            file = get_minio_object(object_name)
            parse_and_save(file)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)
