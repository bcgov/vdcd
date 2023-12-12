from django_q.tasks import schedule
from django.db import IntegrityError


def schedule_create_minio_bucket():
    try:
        schedule(
            "workers.tasks.create_minio_bucket",
            name="create_minio_bucket",
            schedule_type="O",
            repeats=1,
        )
    except IntegrityError:
        pass


def schedule_batch_decode_vins():
    try:
        schedule(
            "workers.tasks.batch_decode_vins",
            50,
            "vpic",
            name="batch_decode_vins",
            schedule_type="C",
            cron="* * * * *",
            q_options={"timeout": 60, "ack_failure": True},
        )
    except IntegrityError:
        pass
