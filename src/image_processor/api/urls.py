from django.urls import path

from ..api.views import BackgroundRemovalAPIView

urlpatterns = [
    path('remove-background/', BackgroundRemovalAPIView.as_view(), name='remove-background')
]
