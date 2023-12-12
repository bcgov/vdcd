from rest_framework import routers
from api.viewsets.uploaded_vin_record import UploadedVinRecordViewset
from api.viewsets.decoded_vin_record import DecodedVinRecordViewset
from api.viewsets.healthcheck import HealthCheckViewset

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"healthcheck", HealthCheckViewset, basename="healthcheck")
router.register(r"uploaded-vin-records", UploadedVinRecordViewset)
router.register(r"decoded-vin-records", DecodedVinRecordViewset)
urlpatterns = router.urls
