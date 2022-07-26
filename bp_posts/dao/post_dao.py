import json
from json import JSONDecodeError

from bp_posts.dao.post import Post
from exceptions.data_exceptions import DataSourceError


class PostDAO:

    def __init__(self, path):
        self.path = path

    def _load_data(self):

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f"Не удается получить данные из файла {self.path}")

        return posts_data

    def _load_posts(self):

        posts_data = self._load_data()
        list_of_posts = [Post(**post_data) for post_data in posts_data]
        return list_of_posts

    def get_all(self):

        posts = self._load_posts()
        return posts

    def get_by_pk(self, pk):

        if type(pk) != int:
            raise TypeError("pk must be an int")

        posts = self._load_posts()
        for post in posts:
            if post.pk == pk:
                return post

    def search_in_content(self, substring):

        if type(substring) != str:
            raise TypeError("substring must be an str")

        substring = substring.lower()
        posts = self._load_posts()

        matching_posts = [post for post in posts if substring in post.content.lower()]

        return matching_posts

    def get_by_poster(self, user_name):

        if type(user_name) != str:
            raise TypeError("user_name must be an str")

        user_name = str(user_name).lower()
        posts = self._load_posts()

        matching_posts = [post for post in posts if post.poster_name.lower() == user_name]

        return matching_posts

