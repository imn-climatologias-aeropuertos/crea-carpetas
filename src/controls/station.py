from typing import List

import flet as ft

from pydantic import BaseModel

from config import Colors


class Station(BaseModel):
    short_name: str
    name: str
    icao: str
    abrev: str
    tel: str
    fax: str


stations = {
    "Alajuela": {
        "short_name": "Alajuela",
        "name": "Aeropuerto Internacional Juan Santamaría",
        "icao": "MROC",
        "abrev": "AIJS",
        "tel": "(506) 2441-2398",
        "fax": "(506) 2442-7036",
    },
    "Liberia": {
        "short_name": "Liberia",
        "name": "Aeropuerto Internacional Daniel Oduber Quirós",
        "icao": "MRLB",
        "abrev": "AIDOQ",
        "tel": "(506) 2668-1156",
        "fax": "(506) 2668-1178",
    },
    "Pavas": {
        "short_name": "Pavas",
        "name": "Aeropuerto Internacional Tobías Bolaños Palma",
        "icao": "MRPV",
        "abrev": "AITBP",
        "tel": "(506) 2232-2071",
        "fax": "",
    },
    "Limon": {
        "short_name": "Limón",
        "name": "Aeropuerto Internacional de Limón",
        "icao": "MRLM",
        "abrev": "AIL",
        "tel": "(506) 2758-0480",
        "fax": "",
    },
}


def get_stations() -> List[ft.DropdownOption]:
    station_options = []

    for station in stations.keys():
        station_options.append(
            ft.DropdownOption(
                key=station,
                content=ft.Text(
                    value=station,
                    color=Colors.black,
                    size=20,
                ),
            )
        )

    return station_options


class StationDropdown(ft.Dropdown):
    def __init__(self, on_change):
        stations = get_stations()
        super().__init__(
            enable_filter=True,
            options=stations,
            editable=True,
            on_change=on_change,
            label="Estación",
            value=stations[0].key,
        )

    @property
    def station(self) -> Station:
        d = stations.get(self.value)
        return Station(**d)
