from django.conf.urls import url, include
from .views import Toplist

urlpatterns = [
    url(r'', Toplist.as_view(), name='toplist'),
]
