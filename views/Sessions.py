from views.Base import BaseTable
import flet as ft
import logging
from helper import fetch_all

class Sessions(BaseTable):
    def __init__(self, page: ft.Page, db_path):
        super().__init__(page, db_path)
        self.data_table.columns = [
            ft.DataColumn(label=ft.Text("Фильм")),
            ft.DataColumn(label=ft.Text("Время")),
            ft.DataColumn(label=ft.Text("Зал")),
        ]
        self.load_genres()

    def load_genres(self):
        self.load_data(
            """
                SELECT  m.Title
                       , s.SessionTime 
                       , s.Hall
                FROM tblSessions s JOIN 
                        tblMovies m ON m.MovieID = s.MovieID
                ORDER BY m.Title
            """)


