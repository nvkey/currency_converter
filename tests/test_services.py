import pytest
from rest_framework.test import APIClient

from api.services import CacheDataService as Cds
from exchange_rate.models import DataCurrencyCache


def express_currency(currency: DataCurrencyCache):
    """Метод выражения класса Artist"""
    return {
        "name": currency.name,
        "conversion_rate": currency.conversion_rate,
    }


@pytest.mark.django_db(transaction=True)
class TestCacheDataService:
    def test_create_list_objects(self):
        obj_dict = {
            "USD": 1,
        }
        new_data = Cds.create_list_objects(obj_dict)[0]
        actual = express_currency(new_data)
        expected = {
            "name": "USD",
            "conversion_rate": 1,
        }
        assert expected == actual

    def test_create_data_models(self):
        data_objs_list = [DataCurrencyCache(name="USD", conversion_rate=1)]
        expected = Cds.create_data_models(data_objs_list)[0]
        actual = DataCurrencyCache.objects.last()
        assert expected == actual


@pytest.mark.django_db(transaction=True)
def test_calc_conversion(api_client: APIClient):
    DataCurrencyCache.objects.update_or_create(name="USD", conversion_rate=1)
    DataCurrencyCache.objects.update_or_create(name="AED", conversion_rate=2)
    url = "/api/v1/pair/USD/AED/5"
    actual = api_client.get(url).data
    expected = {
        "base_code": "USD",
        "target_code": "AED",
        "conversion_rate": 2,
        "conversion_result": 10,
    }
    assert expected == actual
