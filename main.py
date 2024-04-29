import base64
import os
from concurrent.futures import ThreadPoolExecutor

import requests

url = 'http://127.0.0.1:8000/api/image-process/remove-background/'


def process_image(image_file):
    picture_id = os.path.splitext(image_file)[0]

    with open(os.path.join('images', image_file), 'rb') as f:
        picture_base64 = base64.b64encode(f.read()).decode('utf-8')

    data = {
        'picture_id': picture_id,
        'picture': picture_base64
    }

    response = requests.post(url, data=data)
    status_code = response.status_code
    if status_code == 200:
        print(f'Picture {picture_id} background removed successfully!')
    else:
        print(f'Failed to remove background for picture {picture_id}!')


if __name__ == '__main__':
    image_files = os.listdir('images')

    with ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(process_image, image_files)
