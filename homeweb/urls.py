from django.conf.urls import url
from .views import homeweb

urlpatterns = [
    url(r'^$', homeweb.as_view(), name='index'),
]
