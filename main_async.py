import os
import time
import asyncio
from io import BytesIO

import aiofiles
from PIL import Image
from loguru import logger

processed_images_count = 0

logger.add('/data/logs/{time}.log', format='{time} {level} {message}', level='ERROR')


def collect_images(path: str) -> list:
    images = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            images.extend(collect_images(file_path))
        else:
            if file.endswith(('.png', '.jpg', '.jpeg', '.webp')):
                images.append(file_path)
    return images


async def process_image(file_path):
    global processed_images_count
    logger.info(
        f'{file_path=} | Successfully processed file. [{processed_images_count}]')

    try:
        img = Image.open(file_path)
        img.thumbnail((800, 800))
        img.save(file_path, quality=60)
        processed_images_count += 1
    except IOError:
        os.remove(file_path)


async def main():
    start = time.time()
    image_folder = r"E:\Grabber\titles\.ijiranaide nagatoro-san\breasts"
    image_files = collect_images(image_folder)

    tasks = [process_image(file) for file in image_files]
    await asyncio.gather(*tasks)
    end = time.time() - start
    print(
        f"{processed_images_count} Images processed by {end:8.2f} secs. Avg: {processed_images_count / end:8.2f} img/sec.")


if __name__ == "__main__":
    asyncio.run(main())
