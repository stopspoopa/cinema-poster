import flet as ft
from helper import fetch_all, fetch_one, execute_query, check_and_create_db as create_

class MovieApp(ft.UserControl):
    def __init__(self, db_path):
        super().__init__()
        self.db_path = db_path

    def build(self):
        # Fields for the form
        self.title = ft.TextField(label="Title", width=300)
        self.description = ft.TextField(label="Description", width=300)
        self.genre = ft.Dropdown(label="Genre", width=300)
        self.duration = ft.TextField(label="Duration (minutes)", width=300)
        self.age_rating = ft.TextField(label="Age Rating", width=300)
        self.poster_url = ft.TextField(label="Poster URL", width=300)
        self.trailer_url = ft.TextField(label="Trailer URL", width=300)
        self.message = ft.Text()

        # Buttons
        save_button = ft.ElevatedButton(text="Save", on_click=self.save_movie)
        update_button = ft.ElevatedButton(text="Update", on_click=self.update_movie)
        delete_button = ft.ElevatedButton(text="Delete", on_click=self.delete_movie)

        # List view for displaying movies
        self.movie_list = ft.ListView(expand=True)

        return ft.Column(
            controls=[
                self.title,
                self.description,
                self.genre,
                self.duration,
                self.age_rating,
                self.poster_url,
                self.trailer_url,
                ft.Row(controls=[save_button, update_button, delete_button]),
                self.movie_list,
                self.message
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def did_mount(self):
        self.load_genres()
        self.load_movies()

    def load_genres(self):
        genres = fetch_all(self.db_path, "SELECT GenreID, GenreName FROM tblRefGenres")
        self.genre.options = [ft.dropdown.Option(str(genre[0]), genre[1]) for genre in genres]
        self.update()

    def load_movies(self):
        # Load movie list
        movies = fetch_all(self.db_path, "SELECT MovieID, Title FROM tblMovies")
        self.movie_list.controls = [
            ft.TextButton(text=movie[1], on_click=lambda e, movie_id=movie[0]: self.select_movie(movie_id))
            for movie in movies
        ]
        self.update()

    def select_movie(self, movie_id):
        movie = fetch_one(self.db_path, "SELECT * FROM tblMovies WHERE MovieID = ?", (movie_id,))
        if movie:
            self.title.value = movie[1]
            self.description.value = movie[2]
            self.genre.value = str(movie[3])
            self.duration.value = str(movie[4])
            self.age_rating.value = movie[5]
            self.poster_url.value = movie[6]
            self.trailer_url.value = movie[7]
            self.update()

    def save_movie(self, e):
        query = "INSERT INTO tblMovies (Title, Description, GenreID, Duration, AgeRating, PosterURL, TrailerURL) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params = (self.title.value, self.description.value, int(self.genre.value), int(self.duration.value), self.age_rating.value, self.poster_url.value, self.trailer_url.value)
        execute_query(self.db_path, query, params)
        self.message.value = "Movie saved successfully!"
        self.load_movies()
        self.update()

    def update_movie(self, e):
        selected_movie_id = self.get_selected_movie_id()
        if selected_movie_id:
            query = "UPDATE tblMovies SET Title = ?, Description = ?, GenreID = ?, Duration = ?, AgeRating = ?, PosterURL = ?, TrailerURL = ? WHERE MovieID = ?"
            params = (self.title.value, self.description.value, int(self.genre.value), int(self.duration.value), self.age_rating.value, self.poster_url.value, self.trailer_url.value, selected_movie_id)
            execute_query(self.db_path, query, params)
            self.message.value = "Movie updated successfully!"
            self.load_movies()
            self.update()

    def delete_movie(self, e):
        selected_movie_id = self.get_selected_movie_id()
        if selected_movie_id:
            query = "DELETE FROM tblMovies WHERE MovieID = ?"
            execute_query(self.db_path, query, (selected_movie_id,))
            self.message.value = "Movie deleted successfully!"
            self.load_movies()
            self.update()

    def get_selected_movie_id(self):
        # Logic to get the selected movie ID
        # For now, the `select_movie` method already handles updating the fields when a movie is selected.
        # We will use that logic to perform operations like Update or Delete.
        selected_movie_button = self.movie_list.selected_control
        if selected_movie_button:
            # Assuming `selected_control` gives the TextButton, and movie ID is passed through
            return selected_movie_button.on_click.__defaults__[0]  # Get the `movie_id` from the lambda function passed in load_movies()
        return None


# Functions outside the MovieApp class for Flet app start-up

def start_app(page: ft.Page):
    db_name = 'data.db'
    create_(db_name)  # Use the correct function to initialize the database

    page.title = "Movie Management"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window_width = 600
    page.window_height = 800
    page.window_center()
    page.add(MovieApp(db_name))

def main():
    ft.app(target=start_app)

if __name__ == "__main__":
    main()
