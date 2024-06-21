import importlib.resources as ir
import json
import os
import pathlib

import requests

from root import resources
from root.src.utils import logger


class NYTimesAPI:
    """
    Class to interact with the NY Times API to fetch bestseller lists and books from those lists.
    Requires a config file with the base URL and lists to fetch.
    """

    def __init__(self, config_file: str = "ny_times_config.json") -> None:
        """Initialize the NYTimesAPI object.

        Args:
            config_file: The name of the config file. Defaults to "ny_times_config.json".
        """
        self.api_key, self.base_url, self.lists = self.read_config(config_file)

    def read_config(self, config_file: str) -> tuple[str, str, list[str]]:
        """Read the config file and return the API key, base URL, and lists to fetch.

        Args:
            config_file: The name of the config file.

        Returns:
            The API key for the NY Times API.
            The base URL
            Lists to fetch from the API.

        Raises:
            ValueError: If the NY_TIMES_API_KEY environment variable is not set.
        """
        files = str(ir.files(resources))
        with open(pathlib.Path(files, config_file)) as f:
            data = json.load(f)
        api_key = os.environ.get("NY_TIMES_API_KEY")

        if api_key is None:
            raise ValueError("NY_TIMES_API_KEY environment variable not set")

        base_url = data["base_url"]
        lists = data["lists"]
        return api_key, base_url, lists

    def create_url(self, book_list: str) -> str:
        """Create the URL to fetch a list of books from the NY Times API.

        Args:
            book_list: The name of the list to fetch.

        Returns:
            The URL to fetch the list of books.
        """
        return f"{self.base_url}{book_list}.json?api-key={self.api_key}"

    def fetch_list(self, url: str) -> list[dict]:
        """Fetch a list of books from the NY Times API.

        Args:
            url: The URL to fetch the list of books.

        Returns:
            A list of books from the NY Times API. If an error occurs, an empty list is returned.
        """
        try:
            response = requests.get(url).json()
            return response["results"]["books"]
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch list from NY Times API: {e}")
            return []
        except KeyError as e:
            logger.error(f"Unexpected structure in response: {e}")
            return []

    def parse_books(self, books: list[dict], book_list_name: str) -> list[dict]:
        """Parse the list of books fetched from the NY Times API.

        Args:
            books: A list of books from the NY Times API.
            book_list_name: The name of the list of books.

        Returns:
            A list of parsed books.
        """
        parsed_books = []
        for book in books:
            parsed_books.append(
                {
                    "book_list": book_list_name,
                    "rank": book["rank"],
                    "rank_last_week": book["rank_last_week"],
                    "title": book["title"],
                    "author": book["author"],
                    "publisher": book["publisher"],
                    "description": book["description"],
                    "amazon_product_url": book["amazon_product_url"],
                }
            )
        return parsed_books


def fetch_books(nyapi: NYTimesAPI, book_list_name: str) -> list[dict]:
    """Fetch a list of books from the NY Times API.

    Args:
        nyapi: An instance of the NYTimesAPI class.
        book_list_name: The name of the list of books to fetch.

    Returns:
        A list of books fetched from the NY Times API.
    """
    logger.info(f"Fetching books from NY Times API, list {book_list_name}")
    url = nyapi.create_url(book_list_name)
    books = nyapi.fetch_list(url)
    parsed_books = nyapi.parse_books(books, book_list_name)
    return parsed_books
