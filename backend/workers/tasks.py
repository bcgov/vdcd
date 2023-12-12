from django.conf import settings
from api.services.minio import get_minio_client
from func_timeout import func_timeout, FunctionTimedOut
from api.models import UploadedVinRecord, DecodedVinRecord
from api.utilities.generic import get_map
from api.utilities.field_names_map import get_field_names_map
from workers.external_apis.vpic import batch_decode as vpic_batch_decode
from api.models import VpicFieldPair
from api.services.decoded_vin_record import save_decoded_data


def create_minio_bucket():
    bucket_name = settings.MINIO_BUCKET_NAME
    client = get_minio_client()
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)


def batch_decode_vins(batch_size=50, service="vpic"):
    def inner():
        max_decode_attempts = settings.MAX_DECODE_ATTEMPTS
        uploaded_vin_records = (
            UploadedVinRecord.objects.filter(current_decode_successful=False)
            .filter(number_of_current_decode_attempts__lt=max_decode_attempts)
            .order_by("number_of_current_decode_attempts", "created")[:batch_size]
        )
        uploaded_vins = set()
        for uploaded_record in uploaded_vin_records:
            uploaded_vins.add(uploaded_record.vin)
        vins_to_update = set()
        decoded_records_to_update_map = get_map(
            "vin", DecodedVinRecord.objects.filter(vin__in=uploaded_vins)
        )
        for decoded_vin in decoded_records_to_update_map:
            vins_to_update.add(decoded_vin)
        vins_to_insert = uploaded_vins.difference(vins_to_update)

        if service == "vpic":
            decoded_data = vpic_batch_decode(uploaded_vin_records)
            field_names_map = get_field_names_map(VpicFieldPair.objects.all())

        save_decoded_data(
            uploaded_vin_records,
            vins_to_insert,
            decoded_records_to_update_map,
            decoded_data,
            field_names_map,
        )

    try:
        func_timeout(45, inner)
    except FunctionTimedOut:
        print("batch decode vins job timed out")
        raise Exception
