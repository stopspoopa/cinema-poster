from views.Base import BaseTable
import flet as ft
import logging
from helper import fetch_all

class RefUsers(BaseTable):
    def __init__(self, page: ft.Page, db_path):
        super().__init__(page, db_path)
        self.data_table.columns = [
            ft.DataColumn(label=ft.Text("Имя пользователя")),
            ft.DataColumn(label=ft.Text("Электр. почта")),
            ft.DataColumn(label=ft.Text("Роль")),
        ]
        self.load_genres()

    def load_genres(self):
        self.load_data(
            """
                SELECT  u.UserName
                       , u.Email 
                       , r.RoleName
                FROM tblRefUsers u JOIN 
                        tblRefRole r ON r.RoleID = u.RoleID
                ORDER BY u.UserName
            """)


