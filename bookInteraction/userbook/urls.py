from django.urls import path
from .views import BookUserAPIView

urlpatterns = [
    path("like", BookUserAPIView.as_view({
        'post':'like'
    })),
    path("read", BookUserAPIView.as_view({
        'post':'read'
    })),
]