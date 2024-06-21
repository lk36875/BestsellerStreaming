import os
from unittest.mock import patch

import pytest
import requests_mock

from root.src.api.ny_times import NYTimesAPI


@pytest.fixture
def mock_req():
    with requests_mock.Mocker() as m:
        yield m


def test_read_config():
    nyapi = NYTimesAPI("test_config.json")
    assert nyapi.base_url == "https://test.com/"


def test_create_url():
    with patch.dict(os.environ, {"NY_TIMES_API_KEY": "mock_value"}):
        nyapi = NYTimesAPI("test_config.json")
        url = nyapi.create_url("test_list1")
        assert url == "https://test.com/test_list1.json?api-key=mock_value"


def test_fetch_list(mock_req):
    mock_req.get("https://test.com/test_list1.json?api-key=test_key", json={"results": {"books": ["b1", "b2"]}})
    nyapi = NYTimesAPI("test_config.json")
    books = nyapi.fetch_list("https://test.com/test_list1.json?api-key=test_key")
    assert books == ["b1", "b2"]


def test_parse_books():
    nyapi = NYTimesAPI("test_config.json")
    books = [
        {
            "rank": 1,
            "rank_last_week": 0,
            "title": "test_title",
            "author": "test_author",
            "publisher": "test_publisher",
            "description": "test_description",
            "amazon_product_url": "test_url",
        }
    ]
    parsed_books = nyapi.parse_books(books, "test_list1")
    assert parsed_books == [
        {
            "book_list": "test_list1",
            "rank": 1,
            "rank_last_week": 0,
            "title": "test_title",
            "author": "test_author",
            "publisher": "test_publisher",
            "description": "test_description",
            "amazon_product_url": "test_url",
        }
    ]
