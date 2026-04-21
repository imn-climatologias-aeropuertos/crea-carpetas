import asyncio
import os

from abc import ABC
from datetime import datetime
from pathlib import Path
from typing import List

import requests

from .sigwx import create_dirs, SAVE_DATA_PATH


class AviationWeatherWindTempUrl(ABC):
    _base = "https://aviationweather.gov/data/products/fax/FXX_wind_YYY_REGION.gif"
    _americas = "a"
    _ames_africa = "b1"

    @property
    def americas(self):
        return self._base.replace("REGION", self._americas)

    @property
    def ames_africa(self):
        return self._base.replace("REGION", self._ames_africa)


class TurkishHezarfenWindTempUrl(ABC):
    _base = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=CEVIR&syol=PWREGIONYYY_XX00.png"
    _americas = "NE"
    _ames_africa = "AE"

    @property
    def americas(self):
        return self._base.replace("CEVIR", "0").replace("REGION", self._americas)

    @property
    def ames_africa(self):
        return self._base.replace("CEVIR", "1").replace("REGION", self._ames_africa)


FORECAST_HOURS = [6, 12, 18, 24]
LEVELS = {
    "70": "100",
    "40": "240",
    "30": "300",
    "25": "340",
    "20": "390",
}


# AVIATION_WEATHER_FLIGHT_LEVELS = ["100", "240", "300", "340", "390"]
# TURKISH_HEZARFEN_FLIGHT_LEVELS = ["70", "40", "30", "25", "20"]
def normalize_hour(hour: int) -> str:
    if hour >= 24:
        hour -= 24

    return f"{hour:02d}"


def forecast_hours(server: str) -> List[str]:
    if server == "aviation_weather":
        return [f"{hour:02d}" for hour in FORECAST_HOURS]

    current_hour = datetime.now().hour

    if current_hour < 4:
        return [f"{hour:02d}" for hour in FORECAST_HOURS]

    if current_hour < 10:
        return [normalize_hour(hour + 6) for hour in FORECAST_HOURS]

    if current_hour < 16:
        return [normalize_hour(hour + 12) for hour in FORECAST_HOURS]

    if current_hour < 22:
        return [normalize_hour(hour + 18) for hour in FORECAST_HOURS]


def download_wind_temp_maps_sync(
    base_url: str, region: str, server: str = "aviation_weather"
):
    create_dirs()
    hours = forecast_hours(server)

    for key, value in LEVELS.items():
        if server == "aviation_weather":
            level = value
        else:
            level = key

        temp_url = base_url.replace("YYY", level)

        level = value

        for hour, fhour in zip(hours, FORECAST_HOURS):
            url = temp_url.replace("XX", hour)
            response = requests.get(url)
            response.raise_for_status()

            output_path = (
                SAVE_DATA_PATH + f"{region.upper()}_FL{level}_+{fhour:02d}_WINDTEMP.jpg"
            )
            with open(output_path, "wb") as f:
                f.write(response.content)

            print(f"Imagen guardada en: {output_path}.")


async def download_wind_temp_maps_async(need_europe_maps: bool):
    try:
        await asyncio.to_thread(
            download_wind_temp_maps_sync,
            AviationWeatherWindTempUrl().americas,
            "americas",
        )
        if need_europe_maps:
            await asyncio.to_thread(
                download_wind_temp_maps_sync,
                AviationWeatherWindTempUrl().ames_africa,
                "ames_africa",
            )
    except requests.exceptions.RequestException:
        try:
            await asyncio.to_thread(
                download_wind_temp_maps_sync,
                TurkishHezarfenWindTempUrl().americas,
                "americas",
                server="hezarfen",
            )
            if need_europe_maps:
                await asyncio.to_thread(
                    download_wind_temp_maps_sync,
                    TurkishHezarfenWindTempUrl().ames_africa,
                    "ames_africa",
                    server="hezarfen",
                )
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Error al descargar los mapas de viento y temperatura de AviationWeather y Hezarfen: {e}"
            )
