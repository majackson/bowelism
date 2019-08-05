from django.shortcuts import render


def homepage(request):
    return render(request, 'index.html', context={
        'remote_ip': request.META['REMOTE_ADDR']
    })
