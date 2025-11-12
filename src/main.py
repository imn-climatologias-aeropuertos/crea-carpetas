import flet as ft


from __version__ import version
from controls import StationDropdown, Station
from config import Colors


def main(page: ft.Page):
    station: Station

    def dropdown_changed(e):
        station = station_dropdown.station
        page.update()

    station_dropdown = StationDropdown(on_change=dropdown_changed)
    page.add(
        ft.Row(
            [
                station_dropdown,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )


ft.app(main)
