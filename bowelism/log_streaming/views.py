from django.shortcuts import render


def homepage(request):
    if 'bowelism' in request.path:
        content = 'bowelism'
    elif 'user-manual' in request.path:
        content = 'user-manual'
    else:
        content = 'intro'

    return render(request, 'index.html', context={
        'remote_ip': request.META.get('HTTP_X_FORWARDED_FOR') or request.META['REMOTE_ADDR'],
        'content': content
    })
