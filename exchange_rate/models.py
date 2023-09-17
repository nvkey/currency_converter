from django.db import models


class DataCurrencyCache(models.Model):
    name = models.CharField(
        max_length=3,
        verbose_name="Тикер валюты",
        unique=True,
    )
    conversion_rate = models.DecimalField(
        "Коэффициент обмена",
        max_digits=12,
        decimal_places=6,
    )
    updated_date = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"
