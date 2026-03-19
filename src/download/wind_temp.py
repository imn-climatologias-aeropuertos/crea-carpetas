import asyncio
import os

from pathlib import Path

import requests

from .sigwx import create_dirs, SAVE_DATA_PATH

WIND_TEMP_BASE_AMERICAS_URL = (
    "https://aviationweather.gov/data/products/fax/FXX_wind_YYY_a.gif"
)
WIND_TEMP_BASE_EURO_AFR_URL = (
    "https://aviationweather.gov/data/products/fax/FXX_wind_YYY_b1.gif"
)
FORECAST_HOURS = ["06", "12", "18", "24"]
FLIGHT_LEVELS = ["100", "240", "300", "340", "390"]


def download_wind_temp_maps_sync(base_url: str, region: str):
    create_dirs()
    try:
        for level in FLIGHT_LEVELS:
            temp_url = base_url.replace("YYY", level)
            for hour in FORECAST_HOURS:
                url = temp_url.replace("XX", hour)
                response = requests.get(url)
                response.raise_for_status()

                output_path = (
                    SAVE_DATA_PATH + f"FL{level}_+{hour}_WINDTEMP_{region.upper()}.jpg"
                )
                with open(output_path, "wb") as f:
                    f.write(response.content)

                print(f"Imagen guardada en: {output_path}.")
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")


async def download_wind_temp_maps_async(need_europe_maps: bool):
    await asyncio.to_thread(
        download_wind_temp_maps_sync, WIND_TEMP_BASE_AMERICAS_URL, "americas"
    )
    if need_europe_maps:
        await asyncio.to_thread(
            download_wind_temp_maps_sync, WIND_TEMP_BASE_EURO_AFR_URL, "euroafr"
        )
