from api.models import DecodedVinRecord, UploadedVinRecord
from api.utilities.decoded_vin_record import (
    get_decoded_record_to_insert,
    transform_decoded_record_to_update,
)
from django.db import transaction


@transaction.atomic
def save_decoded_data(
    uploaded_vin_records,
    vins_to_insert,
    decoded_records_to_update_map,
    decoded_data,
    field_names_map,
):
    decoded_records_to_insert = []
    decoded_records_to_update = []
    successful_records = decoded_data["successful_records"]
    failed_vins = decoded_data["failed_vins"]

    for uploaded_record in uploaded_vin_records:
        vin = uploaded_record.vin
        if vin in successful_records:
            decoded_datum = successful_records.get(vin)
            uploaded_record.current_decode_successful = True
            if vin in vins_to_insert:
                decoded_records_to_insert.append(
                    get_decoded_record_to_insert(vin, decoded_datum, field_names_map)
                )
            elif vin in decoded_records_to_update_map:
                decoded_record_to_update = decoded_records_to_update_map.get(vin)
                transform_decoded_record_to_update(
                    decoded_record_to_update, decoded_datum, field_names_map
                )
                decoded_records_to_update.append(decoded_record_to_update)

        elif vin in failed_vins:
            uploaded_record.current_decode_successful = False
        uploaded_record.number_of_current_decode_attempts = (
            uploaded_record.number_of_current_decode_attempts + 1
        )

    DecodedVinRecord.objects.bulk_update(
        decoded_records_to_update, ["modified", *field_names_map.values()]
    )
    DecodedVinRecord.objects.bulk_create(decoded_records_to_insert)
    UploadedVinRecord.objects.bulk_update(
        uploaded_vin_records,
        ["modified", "current_decode_successful", "number_of_current_decode_attempts"],
    )


def get_decoded_vins(vins):
    result = {}
    records = DecodedVinRecord.objects.filter(vin__in=vins).values()
    for record in records:
        vin = record["vin"]
        del record["vin"]
        result[vin] = record
    return result
