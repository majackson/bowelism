from django.shortcuts import render


def homepage(request):
    return render(request, 'index.html', context={
        'remote_ip': request.META.get('HTTP_X_FORWARDED_FOR') or request.META['REMOTE_ADDR']
    })
