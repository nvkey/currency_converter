import time

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db(transaction=True)
class TestUrls:
    @pytest.mark.parametrize(
        "url, expectation",
        [
            ("/api/v1/currency/", status.HTTP_200_OK),
            ("/api/v1/pair/AED/USD/2", status.HTTP_200_OK),
            ("/api/v1/open_erapi/USD/", status.HTTP_200_OK),
            ("/api/v1/open_erapi/pair/USD/USD/1", status.HTTP_200_OK),
            ("/admin/", status.HTTP_302_FOUND),
        ],
    )
    def test_api_urls(self, api_client: APIClient, url, expectation):
        time.sleep(1)
        response = api_client.get(url)
        assert response.status_code == expectation
