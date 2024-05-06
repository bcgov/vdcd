from api.models import UploadedVinsFile


def create_vins_file(filename, **kwargs):
    UploadedVinsFile.objects.create(filename=filename, **kwargs)
