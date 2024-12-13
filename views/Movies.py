from views.Base import BaseTable
import flet as ft
import logging
from helper import fetch_all

class Movies(BaseTable):
    def __init__(self, page: ft.Page, db_path):
        super().__init__(page, db_path)
        self.data_table.columns = [
            ft.DataColumn(label=ft.Text("Название фильма")),
            ft.DataColumn(label=ft.Text("Описание")),
            ft.DataColumn(label=ft.Text("Жанр")),
            ft.DataColumn(label=ft.Text("Описание жанра")),
            ft.DataColumn(label=ft.Text("Продолжительность")),
            ft.DataColumn(label=ft.Text("Рейтинг")),
            ft.DataColumn(label=ft.Text("Постер")),
            ft.DataColumn(label=ft.Text("Трейлер")),
        ]
        self.load_genres()

    def load_genres(self):
        self.load_data(
            """
                SELECT 
                          Title
                        , Description
                        , g.GenreName
                        , g.GenreDescription
                        , Duration
                        , AgeRating
                        , PosterURL
                        , TrailerURL
                FROM tblMovies m
                JOIN tblRefGenres g ON g.GenreID = m.GenreID
                ORDER BY Title
            """)
