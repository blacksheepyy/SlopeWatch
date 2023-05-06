import cv2
import os
from loguru import logger
import re


def natural_sort_key(s, _nsre=re.compile("([0-9]+)")):
    return [
        int(text) if text.isdigit() else text.lower()
        for text in _nsre.split(s)
    ]


def video_converter(path: str, output_dir: str = "."):
    # Directory containing the .jpg images
    img_dir = path

    # Get the list of image filenames
    # img_files = sorted(os.listdir(img_dir))
    img_files = sorted(os.listdir(img_dir), key=natural_sort_key)

    # Open the first image to get image size
    img_path = os.path.join(img_dir, img_files[0])
    img = cv2.imread(img_path)
    height, width, channels = img.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"h264")

    # Extract the datetime only for file naming
    name_extracted = path.split("/")[-1]
    video = cv2.VideoWriter(
        f"{output_dir}/{name_extracted}.mp4", fourcc, 5.0, (width, height)
    )

    # Loop through each image and add it to the video
    for img_file in img_files:
        img_path = os.path.join(img_dir, img_file)
        img = cv2.imread(img_path)
        video.write(img)

    # Release the VideoWriter object
    video.release()
