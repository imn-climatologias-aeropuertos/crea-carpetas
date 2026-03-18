import flet as ft


class CustomContainer(ft.Container):
    def __init__(self, content: ft.Control):
        super().__init__(
            content=content,
            margin=10,
            padding=5,
        )
