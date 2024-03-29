from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

from components.wish import Wish
from datasets.datamanager import DataManager

class WishListApp(ft.UserControl):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.db = DataManager('wishes', ['title', 'achieved'])

    def build(self):
        self.new_wish = ft.TextField(hint_text="Enter a new wish!", expand=True)
        self.wishes = ft.Column()
        for id in self.db.data.index:
            wish = Wish(
                id,
                self.db.data['title'][id],
                self.db.data['achieved'][id],
                app=self
            )
            self.wishes.controls.append(wish)
        self.filter = ft.Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[
                ft.Tab(text='all'),
                ft.Tab(text='pending'),
                ft.Tab(text='achieved')
            ]
        )

        return ft.Column([
            ft.Row([
                self.new_wish,
                ft.FloatingActionButton(
                    icon=ft.icons.ADD,
                    on_click=self.add_clicked
                )
            ]),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.wishes
                ]
            )
        ])
    
    def add_clicked(self, e):
        title = self.new_wish.value.strip()
        if title == '':
            self.page.snack_bar = ft.SnackBar(ft.Text("Title can not be empty"), bgcolor='red')
            self.page.snack_bar.open = True
        else:
            id = self.db.add({'title': title, 'achieved': False})
            wish = Wish(
                id,
                self.new_wish.value,
                False,
                app=self
            )
            self.wishes.controls.append(wish)
            self.new_wish.value = ""
        self.update()
        self.page.update()

    def wish_status_change(self, wish):
        self.db.update(wish.id, 'achieved', wish.achieved)
        self.update()

    def wish_title_change(self, wish):
        title = wish.edit_wish.value.strip()
        if title == '':
            self.page.snack_bar = ft.SnackBar(ft.Text("Title can not be empty"), bgcolor='red')
            self.page.snack_bar.open = True
        else:
            self.db.update(wish.id, 'title', title)
            wish.wish.label = title
            wish.display_view.visible = True
            wish.edit_view.visible = False
            wish.update()
        self.page.update()

    def wish_delete(self, wish):
        self.db.delete(wish.id)
        self.wishes.controls.remove(wish)
        self.update()

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for wish in self.wishes.controls:
            wish.visible = (
                status == 'all'
                or (status == 'achieved' and wish.achieved)
                or (status == 'pending' and wish.achieved == False)
            )
        super().update()

    def tabs_changed(self, e):
        self.update()