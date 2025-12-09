import flet as ft


import db

from __version__ import version
from controls import *
from config import Colors
from db import fetch_by_label


def main(page: ft.Page):
    station: Station
    flight: Flight

    db.create()

    # with open("./trash/vuelos.csv") as f:
    #     for line in f:
    #         line = line.split(",")
    #         db.insert(*line)

    # db.insert(
    #     "LRC618",
    #     "MROC",
    #     "KMIA",
    #     "USSS",
    # )

    def station_dropdown_changed(e):
        station = station_dropdown.station
        page.update()

    def flight_dropdown_changed(e):
        first_arrival_dropdown.clear_options()
        second_arrival_dropdown.clear_options()

        flight = flight_dropdown.flight
        arrivals = flight.arrivals.split(" ")
        first_arrival_dropdown.set_options(*arrivals.copy())
        first_arrival_dropdown.disabled = False
        second_arrival_dropdown.set_options()
        page.update()

    def first_arrival_dropdown_changed(e):
        second_arrival_dropdown.clear_options()

        flight = flight_dropdown.flight
        arrivals = flight.arrivals.split(" ")

        if len(arrivals) > 1:
            arrivals.remove(first_arrival_dropdown.value)
            second_arrival_dropdown.set_options(*arrivals.copy(), autoselect=False)
            second_arrival_dropdown.disabled = False
        page.update()

    station_dropdown = StationDropdown(on_change=station_dropdown_changed)
    flight_dropdown = FlightDropdown(on_change=flight_dropdown_changed)
    first_arrival_dropdown = ArrivalsDropDown(on_change=first_arrival_dropdown_changed)
    second_arrival_dropdown = ArrivalsDropDown(label="Destino 2")

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        station_dropdown,
                        flight_dropdown,
                    ]
                ),
                ft.Column(
                    [
                        first_arrival_dropdown,
                    ]
                ),
                ft.Column(
                    [
                        second_arrival_dropdown,
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
        )
    )


ft.app(main)
