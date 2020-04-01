from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class SaleConfig(AppConfig):
    name = 'sale'

    def ready(self):
        autodiscover_modules('startconsume.py')
