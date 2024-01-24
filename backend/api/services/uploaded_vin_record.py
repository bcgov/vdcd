import pandas as pd
from api.models import UploadedVinRecord
from api.constants import SERVICES, get_service
from django.db import transaction
from django.utils import timezone


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
        vin_record.model_year = (
            vin_map[vin_record.vin] if vin_map[vin_record.vin] != "" else None
        )
        vin_record.modified = timezone.now()
        for service in SERVICES:
            setattr(vin_record, service.CURRENT_DECODE_SUCCESSFUL.value, False)
            setattr(vin_record, service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value, 0)
        uploaded_records_to_update.append(vin_record)

    vins_to_insert = vins.difference(vins_to_update)
    uploaded_records_to_insert = []

    service_kwargs = {}
    for service in SERVICES:
        service_kwargs[service.CURRENT_DECODE_SUCCESSFUL.value] = False
        service_kwargs[service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value] = 0
    for vin in vins_to_insert:
        uploaded_records_to_insert.append(
            UploadedVinRecord(
                vin=vin,
                model_year=vin_map[vin] if vin_map[vin] != "" else None,
                **service_kwargs
            )
        )

    update_fields = ["modified", "model_year"]
    for service in SERVICES:
        update_fields.append(service.CURRENT_DECODE_SUCCESSFUL.value)
        update_fields.append(service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value)
    UploadedVinRecord.objects.bulk_update(uploaded_records_to_update, update_fields)
    UploadedVinRecord.objects.bulk_create(uploaded_records_to_insert)


def get_decode_successful(service_name, uploaded_record):
    service = get_service(service_name)
    if service:
        return getattr(uploaded_record, service.CURRENT_DECODE_SUCCESSFUL.value)


def set_decode_successful(service_name, uploaded_record, value):
    service = get_service(service_name)
    if service:
        setattr(uploaded_record, service.CURRENT_DECODE_SUCCESSFUL.value, value)


def get_number_of_decode_attempts(service_name, uploaded_record):
    service = get_service(service_name)
    if service:
        return getattr(uploaded_record, service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value)


def set_number_of_decode_attempts(service_name, uploaded_record, value):
    service = get_service(service_name)
    if service:
        setattr(uploaded_record, service.NUMBER_OF_CURRENT_DECODE_ATTEMPTS.value, value)
