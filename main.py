import os
import time
from concurrent.futures import ThreadPoolExecutor
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


def process_image(file_path):
    global processed_images_count
    logger.info(
        f'{file_path=} | Successfully processed file. [{processed_images_count}]')
    # Здесь можно добавить код для обработки изображения
    try:
        img = Image.open(file_path)
        img.thumbnail((800, 800))
        img.save(file_path, quality=60)
    except IOError:
        os.remove(file_path)
    processed_images_count += 1


def main():
    main_dir = r"E:\Grabber\titles"
    dirs = [os.path.join(main_dir, d) for d in os.listdir(main_dir) if os.path.isdir(os.path.join(main_dir, d))]
    print(dirs)
    for d in dirs:
        logger.critical(
            f'directory={d} | Processing selected directory. [{processed_images_count}]')
        start = time.time()
        image_files = collect_images(d)

        with ThreadPoolExecutor(max_workers=8) as executor:
            executor.map(process_image, image_files)
        end = time.time()-start
        print(f"{processed_images_count} Images processed by {end:8.2f} secs. Avg: {processed_images_count/end:8.2f} img/sec.")


if __name__ == "__main__":
    main()
