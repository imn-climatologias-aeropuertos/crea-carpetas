import flet as ft


class SigWxMaps(ft.Column):
    def __init__(self):
        self.map00 = ft.CupertinoCheckbox(label="00:00 UTC", value=True)
        self.map06 = ft.CupertinoCheckbox(label="06:00 UTC", value=False)
        self.map12 = ft.CupertinoCheckbox(label="12:00 UTC", value=False)
        self.map18 = ft.CupertinoCheckbox(label="18:00 UTC", value=False)
        super().__init__(
            controls=[
                ft.Text(
                    value="Mapas de tiempo significante",
                    size=20,
                ),
                self.map00,
                self.map06,
                self.map12,
                self.map18,
            ],
            spacing=0.1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


class WindTempMaps(ft.Column):
    def __init__(self):
        self.map00 = ft.CupertinoCheckbox(label="00:00 UTC", value=True)
        self.map06 = ft.CupertinoCheckbox(label="06:00 UTC", value=False)
        self.map12 = ft.CupertinoCheckbox(label="12:00 UTC", value=False)
        self.map18 = ft.CupertinoCheckbox(label="18:00 UTC", value=False)
        super().__init__(
            controls=[
                ft.Text(
                    value="Mapas de viento y temperatura",
                    size=20,
                ),
                self.map00,
                self.map06,
                self.map12,
                self.map18,
            ],
            spacing=0.1,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )


class FlightTypeRadio(ft.Column):
    def __init__(self, on_change: ft.ControlEventHandler[ft.RadioGroup]):
        self.high = ft.Radio(label="Alto", value="1")
        self.low = ft.Radio(label="Bajo", value="2")
        self.radio_group = ft.RadioGroup(
            on_change=on_change,
            value=self.high.value,
            content=ft.Column(
                controls=[
                    self.high,
                    self.low,
                ]
            ),
        )
        self.xygrib = ft.CupertinoCheckbox(
            label="Usar mapa XyGrib",
            value=False,
            disabled=True,
        )
        super().__init__(
            controls=[
                ft.Text(
                    value="Tipo de vuelo",
                    size=20,
                ),
                self.radio_group,
                ft.Text(
                    value="Solo para vuelos bajos",
                    size=20,
                ),
                self.xygrib,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
