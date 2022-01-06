from django.urls import path
from .views import ContentAPIView, BookDetailAPIView

urlpatterns = [
    path("", ContentAPIView.as_view({
        'get':'content',
        'post':'create'
    })),
    path("topcontent", ContentAPIView.as_view({
        'get':'topContent',
    })),
    path("<int:pk>", BookDetailAPIView.as_view({
        'get':'get',
        'put':'put',
        'delete':'delete'
    })),
    path("uploadfile", ContentAPIView.as_view({
        'post':'upload_file'
    })),
]