## Project description

As an IDIR user, upload a spreadsheet containing VINs and periodic job(s) will use the configured decoder(s) to decode them and store the result in the database. Uploaded VINs that have already been decoded will be run against the decoder(s) again.

## Integration

Authorized apps can call certain endpoints to get decoded VIN data. To authorize an app, run the django command:

```sh
create_app_user_and_token <app_name>
```

Then, the app can use the token via the Authorization header: 

```sh
Token <token>
```

## Data Structure

Decoded data are stored as JSON fields; database queries may use JSON operators (https://www.postgresql.org/docs/9.5/functions-json.html) to extract fields of interest, e.g.:

```sh
SELECT data->>'FIELD_1' AS field_1, data ->> 'FIELD_2' as field_2 FROM table;
```

where 'data' is the name of the column containing the JSON, and FIELD_1 and FIELD_2 are keys within the JSON data.