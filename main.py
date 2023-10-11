import flet as ft

from components.wishlistapp import WishListApp

from datasets.datamanager import DataManager

def main(page: ft.Page):
    page.add(WishListApp())

ft.app(target=main)