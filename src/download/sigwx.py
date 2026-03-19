import asyncio
import os

from pathlib import Path

import requests

SIGWX_BASE_AMERICAS_URL = (
    "https://aviationweather.gov/data/products/swh/XX_sigwx_hi_a.gif"
)
SIGWX_BASE_EURO_AFR_URL = (
    "https://aviationweather.gov/data/products/swh/XX_sigwx_hi_b1.gif"
)
SAVE_DATA_PATH = "./storage/img/maps/"
MEAN_SYNOP_HOURS = ["00", "06", "12", "18"]


def create_dirs():
    try:
        os.makedirs(SAVE_DATA_PATH)
    except OSError:
        pass


def download_sigwx_maps_sync(base_url: str, region: str):
    create_dirs()
    try:
        for hour in MEAN_SYNOP_HOURS:
            url = base_url.replace("XX", hour)
            response = requests.get(url)
            response.raise_for_status()

            output_path = SAVE_DATA_PATH + f"{hour}Z_SIGWX_{region.upper()}.jpg"
            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"Imagen guardada en: {output_path}.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")


async def download_sigwx_maps_async(need_europe_maps: bool):
    await asyncio.to_thread(
        download_sigwx_maps_sync, SIGWX_BASE_AMERICAS_URL, "americas"
    )
    if need_europe_maps:
        await asyncio.to_thread(
            download_sigwx_maps_sync, SIGWX_BASE_EURO_AFR_URL, "euroafr"
        )
