from django.urls import reverse

from django.test import Client

from rest_framework import status


def test_heartbeat():
    resp = Client().get(reverse('heartbeat'))
    assert resp.status_code == status.HTTP_200_OK
