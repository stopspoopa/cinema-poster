from views.Base import BaseTable
import flet as ft
import logging
from helper import fetch_all

class RefGenres(BaseTable):
    def __init__(self, page: ft.Page, db_path):
        super().__init__(page, db_path)
        self.data_table.columns = [
            ft.DataColumn(label=ft.Text("Название жанра")),
            ft.DataColumn(label=ft.Text("Описание")),
        ]
        self.load_genres()

    def load_genres(self):
        self.load_data("SELECT GenreName, GenreDescription FROM tblRefGenres ORDER BY GenreName")







