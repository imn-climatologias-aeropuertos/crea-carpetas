import flet as ft


from __version__ import version
from controls import StationDropdown, Station
from config import Colors


def main(page: ft.Page):
    def dropdown_changed(e):
        text.value = f"{station_dropdown.station.name}"
        page.update()

    station_dropdown = StationDropdown(on_change=dropdown_changed)
    text = ft.Text(f"{station_dropdown.station.name}", size=25, color=Colors.primary)
    page.add(
        ft.Row(
            [
                station_dropdown,
                text,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    )


ft.app(main)
