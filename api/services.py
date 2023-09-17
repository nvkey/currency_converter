import json
import os
from datetime import datetime, timedelta
from typing import Iterable, Mapping

import requests
from django.utils import timezone

from config.settings import DATA_DIR
from exchange_rate.models import DataCurrencyCache

from .exceptions import ErApiResponseEception


def get_datetime(seconds: int | float | str) -> datetime:
    """Коенвертирует секунды в дату и время."""
    return datetime.fromtimestamp(float(seconds))


def get_all_exchange_rates_erapi(src):
    """Запрос курса валют open.er-api.com по открытому api"""
    url = f"https://open.er-api.com/v6/latest/{src}"
    data = requests.get(url).json()
    if data["result"] == "success":
        last_updated_datetime = get_datetime(data["time_last_update_unix"])
        exchange_rates = data["rates"]
        return {
            "time_last_update": last_updated_datetime,
            "result": exchange_rates,
        }
    raise ErApiResponseEception


class CacheDataService:
    @staticmethod
    def create_list_objects(data_currency: Mapping) -> Iterable:
        """Создает список объектов CurrencyDataCache на базе словаря."""
        data_objs_list = []
        for name, conversion_rate in data_currency.items():
            data_objs_list.append(
                DataCurrencyCache(
                    name=name,
                    conversion_rate=conversion_rate,
                )
            )
        return data_objs_list

    @staticmethod
    def create_data_models(data_objs_list: Iterable) -> int:
        """Созхдает модели в базе"""
        added_objs = DataCurrencyCache.objects.bulk_create(data_objs_list)
        print(f"Количество созданных объектов: {len(added_objs)}")
        return added_objs

    @staticmethod
    def create_data_cache_usd():
        """Записывает обновленные данные по курсам валют"""
        try:
            response = get_all_exchange_rates_erapi("usd")
        except ErApiResponseEception:
            return print("Ошибка ответа открытого ресурса")
        DataCurrencyCache.objects.all().delete()
        data_currency_usd = response["result"]
        objs_list = CacheDataService.create_list_objects(data_currency_usd)
        added_objs = CacheDataService.create_data_models(objs_list)
        print(len(added_objs))
        return added_objs

    @staticmethod
    def refresh_cache_data() -> bool:
        """Обновляет кэш данных каждый час"""
        if not DataCurrencyCache.objects.all().exists():
            CacheDataService.create_data_cache_usd()
            print("Пустая база обновлена")
            return True
        updated_date = DataCurrencyCache.objects.last().updated_date
        time_refresh = timedelta(hours=1)
        time_now = timezone.now()
        time_period = time_now - updated_date
        if time_period > time_refresh:
            CacheDataService.create_data_cache_usd()
            return True
        print(f"Обночление через {time_refresh-time_period}")
        return False


def get_names_from_json():
    names_list = []
    path = os.path.join(DATA_DIR, "tikers.json")
    with open(path, encoding="utf-8") as file:
        initial_data = json.load(file)
        for data in initial_data:
            names_list.append(data)
    return names_list
