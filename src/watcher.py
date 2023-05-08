import requests
import streamlit as st
import os
import time
from loguru import logger
import datetime
from pathlib import Path
from utils.video_converter import video_converter
from itertools import islice


def download_image(url: str, save_path: str):
    r = requests.get(url)
    with open(save_path, "wb") as f:
        f.write(r.content)


if "toggle_button" not in st.session_state:
    st.session_state["toggle_button"] = False

if "current_date" not in st.session_state:
    st.session_state["current_date"] = ""

st.title("Image Downloader App")

if st.button("Start"):
    st.write("Downloading images...")
    st.session_state["toggle_button"] = not st.session_state.get(
        "toggle_button"
    )
    running = st.session_state.get("toggle_button")
    i = 0
    # Generate folder path only if "start" is pressed not "stop"
    if st.session_state.get("toggle_button"):
        st.session_state["current_date"] = datetime.datetime.now().strftime(
            "%Y_%m_%d_%H_%M_%S"
        )
        # Generate folder dir if not exist
        Path(f"images/{st.session_state.get('current_date')}").mkdir(
            parents=True, exist_ok=True
        )
    while running:
        # url = "https://images.unsplash.com/photo-1551698618-1dfe5d97d256?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8M3x8c2tpfGVufDB8fDB8fA%3D%3D&w=1000&q=80"
        url = "https://webcam.thesnowcentre.com/record/current.jpg"

        save_path = f"images/{st.session_state.get('current_date')}/{i}.jpg"
        download_image(url, save_path)
        i += 1
        time.sleep(0.04)
        running = st.session_state.get("toggle_button")
        logger.debug(f"running?: {running}")
    # If stop button has been toggled then start the conversion
    if not st.session_state.get("toggle_button"):
        logger.debug(st.session_state.get("current_date"))
        st.write("Image download stopped.")
        video_converter(
            path=f"images/{st.session_state.get('current_date')}",
            output_dir="videos/raw",
        )

# assign directory
directory = "videos/converted"
# Max number of videos to show
limit = 10

files = [
    os.path.join(directory, f) for f in os.listdir(directory)
]  # add path to each file
files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

for item in islice(files, limit):
    _, file_extension = os.path.splitext(item)
    
    if file_extension == ".mp4":
        video_file = open(
            item,
            "rb",
        )
        video_bytes = video_file.read()
        st.video(video_bytes)
