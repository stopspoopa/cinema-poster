import flet as ft
from flet import View, Page, ElevatedButton, Text
from views.refGenres import RefGenres
from views.refUsers import RefUsers
from views.Movies import Movies
from views.Sessions import Sessions
from views.Booking import Booking

class MainWindow(ft.Control):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        # Регистрация обработчика изменения маршрута
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        # Переход к текущему маршруту
        self.page.go(self.page.route)

        self.statusBar = ft.Text("Статус: Готово", size=14)
        self.textFile = ft.Text("Файл")
        self.menuItemButtonExit = ft.MenuItemButton(content=ft.Text("Выход"), on_click=self.exit_app)
        self.textRef = ft.Text("Справочники")
        self.menuItemButtonRefGenres = ft.MenuItemButton(content=ft.Text("Справочник жанров"), on_click=self.open_genres)
        self.menuItemButtonRefUsers = ft.MenuItemButton(content=ft.Text("Справочник пользователей"), on_click=self.open_users)
        self.menuItemButtonBooking = ft.MenuItemButton(content=ft.Text("Бронирование"), on_click=self.open_booking)
        self.menuItemButtonSessions = ft.MenuItemButton(content=ft.Text("Сеансы"), on_click=self.open_sessions)
        self.menuItemButtonMovies = ft.MenuItemButton(content=ft.Text("Фильмы"), on_click=self.open_movies)
        self.history = []

    def _get_control_name(self):
        return "main_window"

    def route_change(self, route):
        self.page.views.clear()
        main_view = self.build()
        self.page.views.append(main_view)

        if self.page.route == "/refgenres":
            view = RefGenres(self.page, "data.db").build()
            self.page.views.append(view)
        elif self.page.route == "/refusers":
            view = RefUsers(self.page, "data.db").build()
            self.page.views.append(view)
        elif self.page.route == "/movies":
            view = Movies(self.page, "data.db").build()
            self.page.views.append(view)
        elif self.page.route == "/sessions":
            view = Sessions(self.page, "data.db").build()
            self.page.views.append(view)
        elif self.page.route == "/booking":
            view = Booking(self.page, "data.db").build()
            self.page.views.append(view)





        self.page.update()

    def view_pop(self):
        self.page.views.pop()
        top_view: View = self.page.views[-1]
        self.page.go(top_view.route)

    def build(self,  **kwargs):

        # Создаем главное меню
        menu = ft.MenuBar(
            controls=[
                ft.SubmenuButton(
                    content=self.textFile,
                    controls=[self.menuItemButtonExit]
                ),
                ft.SubmenuButton(
                    content=self.textRef,
                    controls=[
                        self.menuItemButtonRefGenres,
                        self.menuItemButtonRefUsers,
                    ],
                ),
                self.menuItemButtonBooking,
                self.menuItemButtonSessions,
                self.menuItemButtonMovies,
            ]
        )

        # Создаем основное окно
        return ft.View("/main", controls=[
            ft.Column(
                controls=[
                    menu,
                    ft.Container(expand=True),
                    self.statusBar
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            )
        ])

    def exit_app(self, e):
        self.page.window.close()

    def open_genres(self, e):
        self.page.go("/refgenres")

    def open_users(self, e):
        self.page.go("/refusers")

    def open_booking(self, e):
        self.page.go("/booking")

    def open_sessions(self, e):
        self.page.go("/sessions")

    def open_movies(self, e):
        self.page.go("/movies")
