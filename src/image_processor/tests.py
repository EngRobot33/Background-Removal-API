import base64
from io import BytesIO
from PIL import Image
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class BackgroundRemovalAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_background_removal_api(self):
        test_image = Image.new('RGB', (100, 100), color='white')
        buffer = BytesIO()
        test_image.save(buffer, format='PNG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        response = self.client.post(
            path='/api/image-process/remove-background/',
            data={'picture_id': 919456, 'picture': image_base64}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.data
        self.assertIn('picture_id', response_data)
        self.assertIn('picture', response_data)
        self.assertEqual(response_data['picture_id'], 919456)

        decoded_image_data = base64.b64decode(response_data['picture'])
        decoded_image = Image.open(BytesIO(decoded_image_data))
        self.assertEqual(decoded_image.format, 'PNG')

    def test_invalid_picture_id(self):
        test_image = Image.new('RGB', (90, 90), color='white')
        buffer = BytesIO()
        test_image.save(buffer, format='PNG')
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        response = self.client.post(
            path='/api/image-process/remove-background/',
            data={'picture_id': 'hamed', 'picture': image_base64}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_data(self):
        response = self.client.post(
            path='/api/image-process/remove-background/',
            data={}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
