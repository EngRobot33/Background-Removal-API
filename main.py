import requests
import base64
import os

url = 'http://127.0.0.1:8000/api/image-process/remove-background/'

image_files = os.listdir('images')

for index, image_file in enumerate(image_files, start=1):
    picture_id = os.path.splitext(image_file)[0]
    print(picture_id)

    with open(os.path.join('images', image_file), 'rb') as f:
        picture_base64 = base64.b64encode(f.read()).decode('utf-8')

    data = {
        'picture_id': picture_id,
        'picture': picture_base64
    }

    response = requests.post(url, data=data)
    print(response.content)
