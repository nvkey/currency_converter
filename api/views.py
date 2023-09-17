from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from exchange_rate.models import DataCurrencyCache

from .serializers import DataCurrencySerializer
from .services import CacheDataService as Cds
from .services import get_all_exchange_rates_erapi


class CurrencyListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Список кэшируемых данных"""

    queryset = DataCurrencyCache.objects.all()
    serializer_class = DataCurrencySerializer

    def list(self, request, *args, **kwargs):
        Cds.refresh_cache_data()
        return super().list(request, *args, **kwargs)


class OpenAccessErApiView(APIView):
    """Запрос курса валюты с открытого ресурса https://www.exchangerate-api.com/
    по обозначению валюты.
    """

    def get(self, request, ticker):
        currency = get_all_exchange_rates_erapi(ticker)
        return Response(currency)


class ExchangePairUSDView(APIView):
    """Обмен валют через USD."""

    def get(self, request, base_currency, target_currency, amount):
        Cds.refresh_cache_data()
        base_currency = get_object_or_404(DataCurrencyCache, name=base_currency)
        target_currency = get_object_or_404(DataCurrencyCache, name=target_currency)
        exchange_rate = round(((1 / base_currency.conversion_rate) * target_currency.conversion_rate), 4)
        res = round(exchange_rate * int(amount), 4)
        context = {
            "base_code": base_currency.name,
            "target_code": target_currency.name,
            "conversion_rate": exchange_rate,
            "conversion_result": res,
        }
        return Response(context)


class ExchangePairErApiView(APIView):
    """Обмен валют через открытый ресурс."""

    def get(self, request, base_currency, target_currency, amount):
        currency = get_all_exchange_rates_erapi(base_currency)
        exchange_rate = round((currency["result"][target_currency]), 4)

        res = round(round(exchange_rate, 4) * int(amount), 4)
        context = {
            "base_code": base_currency,
            "target_code": target_currency,
            "conversion_rate": exchange_rate,
            "conversion_result": res,
        }
        return Response(context)
