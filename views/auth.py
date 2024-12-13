import flet as ft

from core.style import alert_error_bg
from helper import fetch_one as fetch_one

class UserAuthApp(ft.UserControl):
    def __init__(self, page: ft.Page, db_name):
        super().__init__()
        self.db_name = db_name
        self.page = page

        self.login_error = ft.SnackBar(
            ft.Text(f"Вы указали не правильный логин и пароль", color='#ff0000'),
            bgcolor=alert_error_bg
        )

        self.username = ft.TextField(label="Логин", width=200)
        self.password = ft.TextField(label="Пароль", password=True, can_reveal_password=True, width=200)
        self.message = ft.Text()
        self.login_button = ft.ElevatedButton(text="Авторизация", on_click=self.login)


        # Переход к текущему маршруту
        self.page.go(self.page.route)


    def build(self, **kwargs):

        return ft.View("/", controls=[
            ft.Container(
                ft.Column(
                    controls=[
                        self.username,
                        self.password,
                        ft.Row(
                            controls=[self.login_button],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        self.message
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                alignment=ft.alignment.center
            )
        ])

    def login(self, e):
        username = self.username.value
        password = self.password.value

        if self.authenticate_user(username, password):
            self.message.value = "Успешная авторизация!"
            self.message.color = ft.colors.GREEN
            self.update()
            self.page.go('/main')
        else:
            self.message.value = "Неизвестный логин и/или пароль."
            self.message.color = ft.colors.RED
            self.update()

    def authenticate_user(self, username, password):
        query = "SELECT PasswordHash FROM tblRefUsers WHERE UserName = ?"
        result = fetch_one(self.db_name, query, (username,))

        if result:
            stored_password = result[0]
            return password == stored_password
        return False




