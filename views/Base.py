import flet as ft
import logging
from helper import fetch_all

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BaseTable(ft.Control):
    def __init__(self, page: ft.Page, db_path):
        super().__init__()
        self.page = page
        self.db_path = db_path

        self.search_field = ft.TextField(label="Поиск", width=200)
        self.search_button = ft.ElevatedButton(text="Искать", on_click=self.search)

        self.add_button = ft.ElevatedButton(text="Добавить", on_click=self.add_item)
        self.delete_button = ft.ElevatedButton(text="Удалить", on_click=self.delete_item)
        self.edit_button = ft.ElevatedButton(text="Редактировать", on_click=self.edit_item)
        self.back_button = ft.ElevatedButton(text="Назад", on_click=self.go_back)
        self.data_table = ft.DataTable(
        columns=[],
        rows=[]
        )

    def build(self, **kwargs):
        return ft.View("/base", controls=[
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
                )],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH
            )
        ])

    def search(self, e):
        pass

    def add_item(self, e):
        pass

    def delete_item(self, e):
        pass

    def edit_item(self, e):
        pass

    def go_back(self, e):
        logging.info(f"Текущие представления: {self.page.views}")
        if self.page.views:
            self.page.views.pop()
            logging.info(f"Текущие представления после удаления: {self.page.views}")
            if self.page.views:
                top_view = self.page.views[-1]
                self.page.go(top_view.route)
            else:
                logging.info(f"Сюда")
                self.page.go("/main")
        self.page.update()

    def load_data(self, query):
        data = fetch_all(self.db_path, query)

        if data:
            # Проверяем, если столбцы не заданы, устанавливаем их на основе первой строки данных
            if not self.data_table.columns:
                self.data_table.columns = [ft.DataColumn(label=ft.Text(f"Column {i + 1}")) for i in range(len(data[0]))]
            # Заполняем строки таблицы
            self.data_table.rows = [
                ft.DataRow(cells=[ft.DataCell(ft.Text(str(cell))) for cell in row]) for row in data
            ]
            self.update()