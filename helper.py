import sqlite3
import random
from contextlib import closing
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def connect(db_name):
    """Создает подключение к базе данных и возвращает объект соединения."""
    return sqlite3.connect(db_name)

def execute_query(db_name, query, params=()):
    """Выполняет запрос без возврата данных (например, INSERT, UPDATE, DELETE)."""
    with closing(connect(db_name)) as conn, conn, closing(conn.cursor()) as cursor:
        cursor.execute(query, params)
        conn.commit()

def fetch_all(db_name, query, params=()):
    """Выполняет запрос и возвращает все результаты."""
    with closing(connect(db_name)) as conn, closing(conn.cursor()) as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()

def fetch_one(db_name, query, params=()):
    """Выполняет запрос и возвращает один результат."""
    with closing(connect(db_name)) as conn, closing(conn.cursor()) as cursor:
        cursor.execute(query, params)
        return cursor.fetchone()

def check_and_create_db(db_name):
    """Проверяет наличие файла базы данных и создает его, если он не существует."""
    if not os.path.exists(db_name):
        logging.info(f"Файл {db_name} не найден. Создаем базу данных...")
        create_db(db_name)
    else:
        logging.info(f"Файл {db_name} уже существует.")

def create_db(db_name):
    """Создает структуру базы данных."""
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    # Создание таблицы для хранения информации о жанрах
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tblRefGenres (
        GenreID INTEGER PRIMARY KEY AUTOINCREMENT,
        GenreName TEXT NOT NULL,
        GenreDescription TEXT NOT NULL
    )
    ''')

    genres = [
          ("Драма", "Фильмы, которые сосредоточены на эмоциональных и межличностных конфликтах")
        , ("Комедия", "Фильмы, предназначенные для того, чтобы вызвать смех у зрителей")
        , ("Боевик", "Фильмы с большим количеством экшн - сцен, включая драки, погони и взрывы")
        , ("Фантастика", "Фильмы, основанные на научных или фантастических концепциях, таких как космические путешествия или супергерои")
        , ("Ужасы", "Фильмы, созданные для того, чтобы напугать зрителей, часто с элементами сверхъестественного")
        , ("Триллер", "Фильмы, которые держат зрителей в напряжении, часто с элементами загадки или преступления")
        , ("Мелодрама", "Фильмы, сосредоточенные на романтических отношениях и эмоциональных переживаниях")
        , ("Анимация", "Фильмы, созданные с использованием анимационных технологий, часто ориентированные на детей, но не только")
        , ("Документальный", "Фильмы, основанные на реальных событиях и фактах, часто с образовательной целью")
        , ("Фэнтези", "Фильмы, которые включают магию, мифические существа и вымышленные миры")
     ]
    cursor.executemany('''
         INSERT INTO tblRefGenres 
                    (GenreName, GenreDescription) 
                    VALUES (?, ?)
         ''', genres)

    # Создание таблицы для хранения информации о фильмах
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tblMovies (
        MovieID INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Description TEXT,
        GenreID INTEGER,
        Duration INTEGER, -- Продолжительность в минутах
        AgeRating TEXT,
        PosterURL TEXT,
        TrailerURL TEXT,
        FOREIGN KEY (GenreID) REFERENCES refTblGenres(GenreID)
    )
    ''')

    movies = [
        ("Тихая гавань", "История о женщине, которая находит утешение и любовь в маленьком прибрежном городке.", 1, 120,"PG-13", "https://example.com/poster1.jpg", "https://example.com/trailer1.mp4")

        , ("Путь к себе", "Фильм о мужчине, который отправляется в путешествие, чтобы найти смысл жизни после трагической утраты.", 1, 135,"R", "https://example.com/poster2.jpg", "https://example.com/trailer2.mp4")

        , (
        "Время перемен", "Драма о семье, которая сталкивается с трудностями и находит силы для преодоления всех препятствий.", 1, 110,
        "PG", "https://example.com/poster3.jpg", "https://example.com/trailer3.mp4")

        , (
        "Свет в окне", "История о женщине, которая возвращается в родной город, чтобы разобраться с прошлым и найти новый путь в жизни.", 1, 125,
        "PG-13", "https://example.com/poster4.jpg", "https://example.com/trailer4.mp4")

        , (
        "Последний шанс", "ильм о человеке, который получает возможность изменить свою жизнь и исправить ошибки прошлого.", 1, 140,
        "R", "https://example.com/poster5.jpg", "https://example.com/trailer5.mp4")

        , (
        "Смех до слез", "Группа друзей попадает в нелепые ситуации, пытаясь организовать идеальную вечеринку.", 2, 95,
        "PG-13", "https://example.com/poster6.jpg", "https://example.com/trailer6.mp4")

        , (
        "Соседи сверху", "Семья переезжает в новый дом и обнаруживает, что их соседи - настоящие комики.", 2, 105,
        "PG", "https://example.com/poster7.jpg", "https://example.com/trailer7.mp4")

        , (
        "Веселые каникулы", "Группа студентов отправляется на каникулы и попадает в череду смешных и абсурдных приключений.", 2, 110,
        "PG-13", "https://example.com/poster8.jpg", "https://example.com/trailer8.mp4")

        , (
        "Случайный герой", "Обычный человек становится героем после того, как случайно спасает город от катастрофы.", 2, 100,
        "PG-13", "https://example.com/poster9.jpg", "https://example.com/trailer9.mp4")

        , (
        "Смешные деньги", "Бедный парень неожиданно становится богатым, но деньги приносят ему больше проблем, чем радости.", 2, 115,
        "PG-13", "https://example.com/poster10.jpg", "https://example.com/trailer10.mp4")

        , (
        "Неудачники", "Группа неудачников решает создать свою собственную рок-группу и покорить мир музыки.", 2, 130,
        "PG-13", "https://example.com/poster11.jpg", "https://example.com/trailer11.mp4")

        , (
        "Свадебный переполох", "Пара пытается организовать идеальную свадьбу, но все идет не по плану.", 2, 130,
        "PG-13", "https://example.com/poster12.jpg", "https://example.com/trailer12.mp4")

        , (
            "Любовь на расстоянии", "История о паре, которая пытается сохранить свои отношения, несмотря на расстояние и трудности.", 7, 115,
            "PG-13", "https://example.com/poster13.jpg", "https://example.com/trailer13.mp4")

        , (
            "Сердце в огне", "Фильм о женщине, которая находит любовь после долгих лет одиночества и борьбы с прошлым.", 7, 125,
            "PG-13", "https://example.com/poster14.jpg", "https://example.com/trailer14.mp4")

    ]
    cursor.executemany('''
             INSERT INTO tblMovies (
                          Title,
                          Description,
                          GenreID,
                          Duration,
                          AgeRating,
                          PosterURL,
                          TrailerURL
                      )
                      VALUES (
                          ?,
                          ?,
                          ?,
                          ?,
                          ?,
                          ?,
                          ?)
             ''', movies)

    # Создание таблицы для хранения информации о ролях
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tblRefRole (
        RoleID INTEGER PRIMARY KEY AUTOINCREMENT,
        RoleName TEXT NOT NULL
        )
    ''')

    # Вставка данных в таблицу tblRefRole
    cursor.executemany('''
    INSERT INTO tblRefRole (RoleName) VALUES (?)
        ''', [('Администратор',), ('Зритель',), ('Постоянный зритель',)])

    # Создание таблицы для хранения информации о сеансах
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tblSessions (
        SessionID INTEGER PRIMARY KEY AUTOINCREMENT,
        MovieID INTEGER,
        SessionTime DATETIME,
        Hall TEXT,
        FOREIGN KEY (MovieID) REFERENCES tblMovies(MovieID) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')


    sessions = [
          (1, "11:00", "Зал 1")
        , (2, "13:00", "Зал 1")
        , (3, "15:00", "Зал 1")
        , (1, "11:00", "Зал 2")
        , (2, "15:00", "Зал 2")
        , (5, "17:00", "Зал 2")
        , (7, "19:00", "Зал 3")
        , (9, "21:00", "Зал 3")
        , (1, "23:00", "Зал 3")
        , (2, "17:00", "Зал 1")
        , (4, "13:00", "Зал 1")
        , (11, "12:00", "Зал 1")
        , (12, "15:00", "Зал 1")
        , (13, "14:00", "Зал 2")
        , (14, "22:00", "Зал 3")
        , (3, "20:00", "Зал 3")
        , (4, "18:00", "Зал 3")
        , (8, "16:00", "Зал 2")
        , (10, "14:00", "Зал 2")
        , (11, "11:00", "Зал 1")
        , (12, "13:00", "Зал 1")
    ]
    cursor.executemany('''
         INSERT INTO tblSessions 
                    (MovieID, SessionTime, Hall) 
                    VALUES (?, ?, ?)
         ''', sessions)














    # Создание таблицы для хранения информации о пользователях
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tblRefUsers (
        UserID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName TEXT NOT NULL,
        Email TEXT NOT NULL UNIQUE,
        PasswordHash TEXT NOT NULL,
        RoleId INTEGER, -- Роль пользователя (например, администратор или зритель)
        FOREIGN KEY (RoleId) REFERENCES tblRefRole(RoleID) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    # Вставка 20 произвольных пользователей
    users = [
    ('admin', 'admin@example.com', 'admin', 0)
    ]

    for i in range(1, 20):
        roleId =2 if random.random() < 0.7 else 3
        users.append((f'user{i}', f'user{i}@example.com', 'hashed_password', roleId))

    cursor.executemany('''
        INSERT INTO tblRefUsers (UserName, Email, PasswordHash, RoleId) VALUES (?, ?, ?, ?)
        ''', users)

    # Создание таблицы для хранения информации о бронированиях
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tblBookings (
        BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserID INTEGER,
        SessionID INTEGER,
        BookingTime DATETIME,
        Seats TEXT, -- Места, забронированные пользователем
        FOREIGN KEY (UserID) REFERENCES tblRefUsers(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (SessionID) REFERENCES tblSessions(SessionID) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    connection.commit()
    connection.close()
    logging.info(f"База данных {db_name} успешно создана.")



