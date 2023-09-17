from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .services import get_names_from_json
from .views import (
    CurrencyListViewSet,
    ExchangePairErApiView,
    ExchangePairUSDView,
    OpenAccessErApiView,
)

router = DefaultRouter()
router.register("currency", CurrencyListViewSet, basename="data-currency")


currency_list = get_names_from_json()

url_exchange_usd = r"^v1/pair/(?P<base_currency>{})/(?P<target_currency>{})/(?P<amount>\d+)$".format(
    "|".join(currency_list), "|".join(currency_list)
)
url_exchange_erapi = r"^v1/open_erapi/pair/(?P<base_currency>{})/(?P<target_currency>{})/(?P<amount>\d+)$".format(
    "|".join(currency_list), "|".join(currency_list)
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("v1/open_erapi/<ticker>/", OpenAccessErApiView.as_view(), name="open_erapi"),
    re_path(url_exchange_usd, ExchangePairUSDView.as_view(), name="exchange_usd"),
    re_path(url_exchange_erapi, ExchangePairErApiView.as_view(), name="exchange_usd"),
]

urlpatterns += router.urls
