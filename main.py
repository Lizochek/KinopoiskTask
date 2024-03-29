from MovieParser import MovieParser
from StaffParser import StaffParser
from Neo4jService import Neo4jService
import requests

# API-ключ для Кинопоиска
API_KEY = 'dcac579f-caa9-44c8-9652-9b87da2ebf12'

# Создаем объекты для работы с Neo4j и парсинга данных
neo4j = Neo4jService("neo4j+s://795c2229.databases.neo4j.io", "neo4j", "cQ5ncIxLvxKa1uSz_2Xk19omyJ3rCxcBwp60UPKoCOQ")
movie_parser = MovieParser(API_KEY)
staff_parser = StaffParser(API_KEY)

# Обрабатываем фильмы с id от 356 до 500
for film_id in range(356, 501):
    try:
        # Получаем и обрабатываем данные о фильме
        film = movie_parser.get_film_by_id(film_id)
        parsed_film = movie_parser.parse_film_data(film)
        print(f"Film: {parsed_film}")

        # Добавляем фильм в Neo4j
        neo4j.add_movie(parsed_film['title'])

        # Получаем и обрабатываем данные о съемочной группе
        staff = staff_parser.get_staff_by_film_id(parsed_film['filmId'])
        for person in staff:
            parsed_person = staff_parser.parse_staff_data(person)
            print(f"Staff: {parsed_person}")

            # Добавляем члена съемочной группы в Neo4j
            neo4j.add_person(parsed_person['name'], parsed_person['profession'])

            # Добавляем связь между членом съемочной группы и фильмом в Neo4j
            neo4j.add_relationship(parsed_person['name'], parsed_film['title'], parsed_person['profession2'], parsed_person['description'])

        print("------")
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Закрываем соединение с Neo4j
neo4j.close()
