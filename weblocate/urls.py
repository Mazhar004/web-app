from django.conf.urls import url
from .views import ipToLocation, print_pdf

urlpatterns = [
    url(r'^$', ipToLocation.as_view(), name='index'),
    url(r'^pdf/$', print_pdf, name='pdf'),
]
