from views.Base import BaseTable
import flet as ft
import logging
from helper import fetch_all

class Booking(BaseTable):
    def __init__(self, page: ft.Page, db_path):
        super().__init__(page, db_path)
        self.data_table.columns = [
            ft.DataColumn(label=ft.Text("Посетитель")),
            ft.DataColumn(label=ft.Text("Сеанс")),
            ft.DataColumn(label=ft.Text("Название фильма")),
            ft.DataColumn(label=ft.Text("Продолжительность")),
            ft.DataColumn(label=ft.Text("Время бронирования")),
        ]
        self.load_genres()
        self.movie_combobox = ft.Dropdown(
            label="Выберите фильм",
            options=self.get_movie_options()
        )

        self.datetime_combobox = ft.Dropdown(
            label="Выберите дату и время"
        )

    def build(self, **kwargs):
        return ft.View("/bookings", controls=[
            ft.Column(
                controls=[
                    ft.Container(
                        ft.Row(
                            controls=[self.back_button, self.search_field, self.search_button],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        padding=10
                    ),
                    ft.Container(
                        ft.Row(
                            controls=[self.movie_combobox, self.datetime_combobox],
                            alignment=ft.MainAxisAlignment.START
                        ),
                        padding=10
                    ),
                    ft.Container(
                        content=ft.ListView(
                            controls=[self.data_table],
                            expand=True
                        ),
                        expand=True
                    ),
                    ft.Container(
                        ft.Row(
                            controls=[self.add_button, self.delete_button, self.edit_button],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        padding=10
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            )
        ])

    def get_movie_options(self):
        query = "SELECT MovieID, Title FROM tblMovies ORDER BY Title"
        movies = fetch_all(self.db_path, query)
        return [ft.dropdown.Option(key=str(movie[0]), text=movie[1]) for movie in movies]

    def load_genres(self):
        self.load_data(
            """
                SELECT 
                          u.UserName
                        , s.SessionTime
                        , m.Title
                        , m.Duration
                        , b.BookingTime
                FROM tblBookings b
                JOIN tblRefUsers u ON u.UserID = b.UserID
                JOIN tblSessions s ON s.SessionId = b.SessionId
                JOIN tblMovies m ON s.MovieId = m.MovieID
                ORDER BY b.BookingTime, m.Title, u.UserName  
            """)
