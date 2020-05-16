from django.conf.urls import url
from .views import movie_recommend

urlpatterns = [
    url(r'^$', movie_recommend.as_view(), name='index'),
]
