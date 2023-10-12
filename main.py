import flet as ft

from components.wishlistapp import WishListApp

def main(page: ft.Page):
    page.add(WishListApp(page))
    page.title = 'My Wish List'
    page.update()

ft.app(target=main)