from rest_framework import serializers

from exchange_rate.models import DataCurrencyCache


class DataCurrencySerializer(serializers.ModelSerializer):
    """Просмотр курсов валют в кэшируемых данных."""

    class Meta:
        model = DataCurrencyCache
        fields = ("name", "conversion_rate", "updated_date")
