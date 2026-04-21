import asyncio
import os

from abc import ABC
from pathlib import Path

import requests


class AviationWeatherSigwxUrl(ABC):
    _base = "https://aviationweather.gov/data/products/swh/XX_sigwx_hi_REGION.gif"
    _americas = "a"
    _ames_africa = "b1"

    @property
    def americas(self):
        return self._base.replace("REGION", self._americas)

    @property
    def ames_africa(self):
        return self._base.replace("REGION", self._ames_africa)


class TurkishHezarfenSigwxUrl(ABC):
    _base = "https://hezarfen.mgm.gov.tr/Genel/imgKrtPng.ashx?cevir=CEVIR&syol=REGION_XX00.png"
    _americas = "PGEE07"
    _ames_africa = "PGSE06"

    @property
    def americas(self):
        return self._base.replace("CEVIR", "0").replace("REGION", self._americas)

    @property
    def ames_africa(self):
        return self._base.replace("CEVIR", "1").replace("REGION", self._ames_africa)


SAVE_DATA_PATH = "./storage/img/maps/"
MEAN_SYNOP_HOURS = ["00", "06", "12", "18"]


def create_dirs():
    try:
        os.makedirs(SAVE_DATA_PATH)
    except OSError:
        pass


def download_sigwx_maps_sync(base_url: str, region: str):
    create_dirs()
    url = AviationWeatherSigwxUrl()

    for hour in MEAN_SYNOP_HOURS:
        url = base_url.replace("XX", hour)
        response = requests.get(url)
        response.raise_for_status()

        output_path = SAVE_DATA_PATH + f"{region.upper()}_{hour}Z_SIGWX.jpg"
        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"Imagen guardada en: {output_path}.")


async def download_sigwx_maps_async(need_europe_maps: bool):
    try:
        await asyncio.to_thread(
            download_sigwx_maps_sync, AviationWeatherSigwxUrl().americas, "americas"
        )
        if need_europe_maps:
            await asyncio.to_thread(
                download_sigwx_maps_sync,
                AviationWeatherSigwxUrl().ames_africa,
                "ames_africa",
            )
    except requests.exceptions.RequestException as e:
        try:
            await asyncio.to_thread(
                download_sigwx_maps_sync, TurkishHezarfenSigwxUrl().americas, "americas"
            )
            if need_europe_maps:
                await asyncio.to_thread(
                    download_sigwx_maps_sync,
                    TurkishHezarfenSigwxUrl().ames_africa,
                    "ames_africa",
                )
        except requests.exceptions.RequestException as e:
            raise Exception(
                f"Error al descargar los mapas de tiempo significante de AviationWeather y Hezarfen: {e}"
            )
