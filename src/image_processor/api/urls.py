from django.urls import path

from image_processor.api.views import BackgroundRemovalAPIView

urlpatterns = [
    path('remove-background/', BackgroundRemovalAPIView.as_view(), name='remove-background')
]
