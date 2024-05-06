from minio import Minio
from datetime import timedelta
from django.conf import settings


def get_minio_client():
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_USE_SSL,
    )


def get_minio_put_url(object_name):
    client = get_minio_client()
    return client.presigned_put_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=object_name,
        expires=timedelta(seconds=7200),
    )


def get_minio_object(object_name):
    try:
        client = get_minio_client()
        return client.get_object(settings.MINIO_BUCKET_NAME, object_name)
    except:
        raise
