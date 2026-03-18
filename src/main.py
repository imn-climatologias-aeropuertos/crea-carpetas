import flet as ft


import db.flights as db_fl
import controls as ct

from __version__ import version


def main(page: ft.Page):
    station: ct.Station
    flight: ct.Flight

    db_fl.create()

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

    def flight_radio_changed(e: ft.Event[ft.RadioGroup]):
        flight_type_radio.radio_group.value = e.control.value
        if flight_type_radio.radio_group.value == "2":
            flight_type_radio.xygrib.disabled = False
            flight_type_radio.xygrib.value = True
        else:
            flight_type_radio.xygrib.disabled = True
            flight_type_radio.xygrib.value = False
        page.update()

    station_dropdown = ct.StationDropdown(on_select=station_dropdown_changed)
    flight_dropdown = ct.FlightDropdown(on_select=flight_dropdown_changed)
    first_arrival_dropdown = ct.ArrivalsDropDown(
        on_select=first_arrival_dropdown_changed
    )
    second_arrival_dropdown = ct.ArrivalsDropDown(label="Destino 2")
    add_flight_button = ft.IconButton(icon=ft.Icons.ADD_OUTLINED)
    forecaster_name = ft.TextField(label="Nombre del pronosticador")
    document_serial = ft.TextField(label="Número de documento")
    creation_hour = ft.TextField(label="Hora de emisión (UTC)")
    forecast_flight_hour = ft.TextField(label="Hora del pronóstico de despegue (UTC)")
    qnh = ft.TextField(label="QNH (hPa)")
    wind_dir = ft.TextField(label="Dirección del viento (°)")
    wind_spd = ft.TextField(label="Velocidad del viento (kt)")
    temp = ft.TextField(label="Temperatura (°C)")
    sigwx_maps = ct.SigWxMaps()
    wind_temp_maps = ct.WindTempMaps()
    flight_type_radio = ct.FlightTypeRadio(on_change=flight_radio_changed)
    download_button = ft.FilledButton(
        content="Descargar Mapas",
        icon=ft.Icons.DOWNLOAD_ROUNDED,
        on_click=on_click_download,
    )
    create_button = ft.FilledButton(
        content="Crear carpeta",
        icon=ft.Icons.FOLDER,
    )

    page.window.width = 1000
    page.window.height = 800
    page.bgcolor = ft.Colors.BLACK

    page.add(
        ft.Container(
            border_radius=ft.BorderRadius.all(20),
            content=ft.Row(
                [
                    ct.CustomContainer(
                        content=ft.Column(
                            [
                                station_dropdown,
                                ft.Row(
                                    [
                                        flight_dropdown,
                                        first_arrival_dropdown,
                                        second_arrival_dropdown,
                                        add_flight_button,
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
                            spacing=25,
                        ),
                    ),
                    ct.CustomContainer(
                        content=ft.Column(
                            controls=[
                                sigwx_maps,
                                wind_temp_maps,
                                flight_type_radio,
                                ct.CustomContainer(
                                    content=ft.Column(
                                        controls=[
                                            download_button,
                                            create_button,
                                        ],
                                        spacing=20,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                ],
                spacing=35,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ),
    ),


ft.run(main)
