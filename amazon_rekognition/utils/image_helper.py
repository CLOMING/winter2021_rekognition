import io

from PIL import Image


def get_image_bytes(
    image_path: str,
    quality: int = 100,
) -> bytes:
    image_bytes: bytes

    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        stream = io.BytesIO()
        image.save(stream, quality=quality, format=image.format)
        image_bytes = stream.getvalue()
        image.close()

    if image_bytes == None:
        raise ValueError("image_bytes is None")

    return image_bytes