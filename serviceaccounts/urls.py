from django.urls import path
from .views import test, test2

urlpatterns = [
    path('', test, name = 'test'),
    path('2', test2, name = 'test_bytes_serializer'),
]