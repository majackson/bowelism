from django.http import HttpResponse


def heartbeat(request):
    """
    Just a simple view that returns a 200 response.
    Intended to be use for testing & monitoring of the service.
    """
    return HttpResponse()
