# returns map of external api field names to internal field names
def get_field_names_map(field_pairs):
    result = {}
    for entry in field_pairs:
        result[entry.external_field_name] = entry.internal_field_name
    return result
