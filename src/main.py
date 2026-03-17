import flet as ft


import db.flights as db_fl
import controls as ct

from __version__ import version


def main(page: ft.Page):
    station: ct.Station
    flight: ct.Flight

    db_fl.create()

    # with open("./trash/vuelos.csv") as f:
    #     for line in f:
    #         line = line.split(",")
    #         db_fl.insert(*line)

    # db_fl.insert(
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

    station_dropdown = ct.StationDropdown(on_change=station_dropdown_changed)
    flight_dropdown = ct.FlightDropdown(on_change=flight_dropdown_changed)
    first_arrival_dropdown = ct.ArrivalsDropDown(
        on_change=first_arrival_dropdown_changed
    )
    second_arrival_dropdown = ct.ArrivalsDropDown(label="Destino 2")
    forecaster_name = ft.TextField(label="Nombre del pronosticador")
    document_serial = ft.TextField(label="Número de documento")
    creation_hour = ft.TextField(label="Hora de emisión (UTC)")
    forecast_flight_hour = ft.TextField(label="Hora del pronóstico de despegue (UTC)")
    qnh = ft.TextField(label="QNH (hPa)")
    wind_dir = ft.TextField(label="Dirección del viento (°)")
    wind_spd = ft.TextField(label="Velocidad del viento (kt)")
    temp = ft.TextField(label="Temperatura (°C)")

    page.add(
        ft.Row(
            [
                ft.Column(
                    [
                        station_dropdown,
                        ft.Row(
                            [
                                flight_dropdown,
                                first_arrival_dropdown,
                                second_arrival_dropdown,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                        ),
                        forecaster_name,
                        document_serial,
                        creation_hour,
                        forecast_flight_hour,
                        qnh,
                        wind_dir,
                        wind_spd,
                        temp,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=25,
                ),
            ],
            # alignment=ft.MainAxisAlignment.START,
            # vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


ft.app(main)
