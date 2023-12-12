import pandas as pd
from api.models import UploadedVinRecord
from django.db import transaction


@transaction.atomic
def parse_and_save(file):
    vin_map = {}
    df = pd.read_excel(file)
    df.fillna("", inplace=True)
    for _, row in df.iterrows():
        if row["VIN"] != "":
            vin_map[row["VIN"]] = row["Model Year"]

    vins = set(vin_map.keys())
    already_uploaded_vin_records = UploadedVinRecord.objects.filter(vin__in=vins)
    vins_to_update = set()
    uploaded_records_to_update = []
    for vin_record in already_uploaded_vin_records:
        vins_to_update.add(vin_record.vin)
        vin_record.model_year = vin_map[vin_record.vin] if vin_map[vin_record.vin] != "" else None
        vin_record.current_decode_successful = False
        vin_record.number_of_current_decode_attempts = 0
        uploaded_records_to_update.append(vin_record)

    vins_to_insert = vins.difference(vins_to_update)
    uploaded_records_to_insert = []
    for vin in vins_to_insert:
        uploaded_records_to_insert.append(
            UploadedVinRecord(
                vin=vin,
                model_year=vin_map[vin] if vin_map[vin] != "" else None,
                current_decode_successful=False,
                number_of_current_decode_attempts=0,
            )
        )

    UploadedVinRecord.objects.bulk_update(
        uploaded_records_to_update,
        [
            "modified",
            "model_year",
            "current_decode_successful",
            "number_of_current_decode_attempts",
        ],
    )
    UploadedVinRecord.objects.bulk_create(uploaded_records_to_insert)
