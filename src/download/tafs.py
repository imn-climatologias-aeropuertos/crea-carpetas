import asyncio
import re

from typing import List, Optional

import requests

from pydantic import BaseModel

from db import fetch_by_icao


AVIATION_WEATHER_BASE_URL = (
    "https://aviationweather.gov/api/data/taf?ids=SSSS&format=raw"
)


class FlightIcaoIds(BaseModel):
    departure: str
    arrival_one: str
    arrival_two: Optional[str]


def get_icao_ids_from_db(flight_icao_ids: FlightIcaoIds) -> List[str]:
    icao_ids = [flight_icao_ids.departure, flight_icao_ids.arrival_one]

    fetch_arrival_1 = fetch_by_icao(flight_icao_ids.arrival_one)
    icao_ids = icao_ids + fetch_arrival_1[0][2].split(" ")
    if flight_icao_ids.arrival_two:
        fetch_arrival_2 = fetch_by_icao(flight_icao_ids.arrival_two)
        icao_ids = icao_ids + fetch_arrival_2[0][2].split(" ")
        icao_ids.append(flight_icao_ids.arrival_two)
    icao_ids = list(set(icao_ids))
    icao_ids.sort()

    return icao_ids


def order_tafs(flight_icao_ids: FlightIcaoIds, tafs: List[str]) -> List[str]:
    flight_tafs: List[str] = ["", "", ""]
    tafs.sort()
    tafs = [taf.strip() for taf in tafs]

    for taf in tafs:
        if len(taf.strip()) == 0:
            continue

        if re.search(flight_icao_ids.arrival_one, taf):
            flight_tafs[1] = taf

        if re.search(flight_icao_ids.departure, taf):
            flight_tafs[0] = taf

        if (
            flight_icao_ids.arrival_two is not None
            and len(flight_icao_ids.arrival_two) == 4
        ) and flight_icao_ids.arrival_two in taf:
            flight_tafs[2] = taf

    flight_tafs = [taf.strip() for taf in flight_tafs if taf != ""]
    for taf in flight_tafs:
        tafs.remove(taf)

    if len(flight_tafs) > 0:
        return flight_tafs + tafs
    return tafs


def get_tafs(
    departure_icao: str,
    arrival_one_icao: str,
    arrival_two_icao: Optional[str],
) -> Optional[str]:
    if arrival_two_icao == " ":
        arrival_two_icao = None

    flight_icao_ids = FlightIcaoIds(
        departure=departure_icao,
        arrival_one=arrival_one_icao,
        arrival_two=arrival_two_icao,
    )

    icao_ids = get_icao_ids_from_db(flight_icao_ids)

    try:
        url = AVIATION_WEATHER_BASE_URL.replace("SSSS", "%2C".join(icao_ids))
        response = requests.get(url)
        response.raise_for_status()

        tafs = re.split(r"\n{2,}", response.text.replace("TAF", "\nTAF"))
        tafs = order_tafs(flight_icao_ids, tafs)

        return "\n\n".join(tafs)
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar los TAF's: {e}")
    return


async def get_tafs_async(*stations: Optional[str]):
    tafs = await asyncio.to_thread(get_tafs, *stations)
    return tafs
