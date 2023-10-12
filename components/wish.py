from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Wish(ft.UserControl):
    def __init__(self, id, title, achieved, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        self.title = title
        self.achieved = achieved
        self.app = app

    def build(self):
        self.wish = ft.Checkbox(value=self.achieved, label=self.title, on_change=self.status_changed)
        self.edit_wish = ft.TextField(expand=1)

        self.display_view = ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.wish,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.CREATE_OUTLINED,
                            tooltip='Edit wish',
                            on_click=self.edit_clicked
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE_OUTLINE,
                            tooltip='Delete wish',
                            on_click=self.delete_clicked
                        )
                    ]
                )
            ]
        )

        self.edit_view = ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_wish,
                ft.IconButton(
                    icon=ft.icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.colors.GREEN,
                    tooltip='Save',
                    on_click=self.save_clicked
                ),
                ft.IconButton(
                    icon=ft.icons.CANCEL_OUTLINED,
                    icon_color=ft.colors.RED,
                    tooltip='Cancel',
                    on_click=self.cancel_edit
                )
            ]
        )

        return ft.Column(controls=[self.display_view, self.edit_view])
    
    def edit_clicked(self, e):
        self.edit_wish.value = self.wish.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.app.wish_title_change(self)

    def cancel_edit(self, e):
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()

    def delete_clicked(self, e):
        self.app.wish_delete(self)
    
    def status_changed(self, e):
        self.achieved = self.wish.value
        self.app.wish_status_change(self)