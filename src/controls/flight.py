from typing import List, Callable, Optional

import flet as ft
from pydantic import BaseModel

from config import Colors
from db import fetch_flights


class Flight(BaseModel):
    id: int
    label: str
    departure: str
    arrivals: str


flights_from_db = fetch_flights()


def get_flight_labels_options() -> List[ft.DropdownOption]:
    flight_options = []

    for flight in flights_from_db:
        flight = Flight(
            id=flight[0],
            label=flight[1],
            departure=flight[2],
            arrivals=flight[3],
        )
        flight_options.append(
            ft.DropdownOption(
                key=flight.label,
                content=ft.Text(
                    value=flight.label,
                    color=Colors.black,
                    size=20,
                ),
                data=flight,
            ),
        )
    return flight_options


class FlightDropdown(ft.Dropdown):
    def __init__(self, on_change):
        self.flights = get_flight_labels_options()
        super().__init__(
            enable_filter=True,
            options=self.flights,
            editable=True,
            on_change=on_change,
            label="Vuelo",
            width=200,
        )

    @property
    def flight(self) -> Flight:
        for flight in self.flights:
            if self.value == flight.key:
                return flight.data


class ArrivalsDropDown(ft.Dropdown):
    def __init__(self, on_change: Optional[Callable] = None, label: str = "Destino 1"):
        super().__init__(
            enable_filter=True,
            editable=True,
            disabled=True,
            on_change=on_change,
            label=label,
            width=200,
        )

    def set_options(self, *options: str, autoselect: bool = True):
        self.options.clear()
        self.options.append(
            ft.DropdownOption(
                key=" ",
                content=ft.Text(
                    value=" ",
                    color=Colors.black,
                    size=20,
                ),
            ),
        )
        for option in options:
            self.options.append(
                ft.DropdownOption(
                    key=option,
                    content=ft.Text(
                        value=option,
                        color=Colors.black,
                        size=20,
                    ),
                ),
            )

        if len(options) == 1 and autoselect:
            self.value = options[0]

    def clear_options(self):
        self.options.clear()
        self.disabled = True
        self.value = " "
        self.update()
