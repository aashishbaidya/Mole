from office.models import District, Office


def dcms_data(request):
    return {
        'districts': District.objects.all(),
        'projects': Office.objects.filter(is_project=True)
    }
