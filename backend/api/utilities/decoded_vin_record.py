from api.models import DecodedVinRecord
from django.utils import timezone


# field_names_map should be a map of external api field names to internal db field names
def get_decoded_record_to_insert(vin, decoded_data, field_names_map):
    kwargs = {"vin": vin}
    for external_name, internal_name in field_names_map.items():
        value = decoded_data.get(external_name)
        kwargs[internal_name] = value
    return DecodedVinRecord(**kwargs)


# field_names_map should be a map of external api field names to internal db field names
def transform_decoded_record_to_update(decoded_record, decoded_data, field_names_map):
    decoded_record.modified = timezone.now()
    for external_name, internal_name in field_names_map.items():
        value = decoded_data.get(external_name)
        setattr(decoded_record, internal_name, value)
