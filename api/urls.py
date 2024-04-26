from django.urls import path, include

urlpatterns = [
    path('image-process/', include('image_processor.api.urls')),
]
