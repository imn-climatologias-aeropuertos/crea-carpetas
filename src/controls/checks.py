import flet as ft


class SigWxMaps(ft.Column):
    def __init__(self):
        map00 = ft.CupertinoCheckbox(label="00:00 UTC", value=True)
        map06 = ft.CupertinoCheckbox(label="06:00 UTC", value=False)
        map12 = ft.CupertinoCheckbox(label="12:00 UTC", value=False)
        map18 = ft.CupertinoCheckbox(label="18:00 UTC", value=False)
        super().__init__(
            controls=[
                ft.Text(
                    value="Mapas de tiempo significante",
                ),
                map00,
                map06,
                map12,
                map18,
            ],
            spacing=0.1,
        )


class WindTempMaps(ft.Column):
    def __init__(self):
        map00 = ft.CupertinoCheckbox(label="00:00 UTC", value=True)
        map06 = ft.CupertinoCheckbox(label="06:00 UTC", value=False)
        map12 = ft.CupertinoCheckbox(label="12:00 UTC", value=False)
        map18 = ft.CupertinoCheckbox(label="18:00 UTC", value=False)
        super().__init__(
            controls=[
                ft.Text(
                    value="Mapas de viento y temperatura",
                ),
                map00,
                map06,
                map12,
                map18,
            ],
            spacing=0.1,
        )


class FlightType(ft.Column):
    def __init__(self):
        high = ft.CupertinoRadio(label="Alto", value=True)
        low = ft.CupertinoRadio(label="Bajo", value=False)
        xygrib = ft.CupertinoCheckbox(label="Usar mapa XyGrib", value=False)
        super().__init__(
            controls=[
                ft.Text(
                    value="Tipo de vuelo",
                ),
                high,
                low,
                ft.Text(
                    value="Solo para vuelos bajos",
                ),
                xygrib,
            ],
        )
