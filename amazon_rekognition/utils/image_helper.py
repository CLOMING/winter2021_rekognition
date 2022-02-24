import io
import requests

from PIL import Image


def get_image_bytes(image_path: str, quality: int = 100) -> bytes:
    image_bytes: bytes

    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        stream = io.BytesIO()
        image.save(stream, quality=quality, format=image.format)
        image_bytes = stream.getvalue()
        image.close()

    if not image_bytes:
        raise ValueError("image_bytes is None")

    return image_bytes


def get_image_bytes_from_url(url: str) -> bytes:
    image_bytes: bytes

    response = requests.get(url)
    image_bytes = response.content

    if not image_bytes:
        raise ValueError("image_bytes is None")

    return image_bytes
