from views.auth import UserAuthApp
from helper import check_and_create_db as create_db
import flet as ft
#from flet_route import Routing, path, Params, Basket
import logging
from views.mainWindow import MainWindow
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class Main():
    def __init__(self, page: ft.Page):
        self.page = page
        page.title = "Киноафиша"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.width = 1000
        page.window.height = 1000
        page.window.center()
        db_name = 'data.db'
        create_db(db_name)

        # Регистрация обработчиков событий
        self.page.on_route_change = self.route_change
        # Переход к текущему маршруту
        self.page.go(self.page.route)

    def route_change(self, route):
        if self.page.route == "/":
            auth_view = UserAuthApp(self.page, 'data.db').build()
            self.page.views.clear()
            self.page.views.append(auth_view)
        elif self.page.route == "/main":
            main_view = MainWindow(self.page).build()
            self.page.views.clear()
            self.page.views.append(main_view)
        self.page.update()

if __name__ == "__main__":
    ft.app(target=Main, view=ft.WEB_BROWSER, assets_dir='assets')









