import base64
import os
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from image_processor.api.serializers import ImageSerializer
from image_processor.segmentation_models.tracer_b7 import TracerUniversalB7


class BackgroundRemovalAPIView(APIView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            picture_id = serializer.validated_data.get('picture_id')
            picture_base64 = serializer.validated_data.get('picture')

            image_data = base64.b64decode(picture_base64)
            img = Image.open(BytesIO(image_data))

            tracer = TracerUniversalB7(model_path=settings.TRACER_B7_MODEL_FILE_PATH)
            result = tracer.inference(img)

            buffered = BytesIO()
            result.save(buffered, format="PNG")
            result_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            result_directory = settings.MEDIA_ROOT
            if not os.path.exists(result_directory):
                os.makedirs(result_directory)

            result_image_path = os.path.join(result_directory, f"{picture_id}_removed_background.png")
            with open(result_image_path, "wb") as result_file:
                result_file.write(buffered.getvalue())

            return Response(
                data={
                    'picture_id': picture_id,
                    'picture': result_base64
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
