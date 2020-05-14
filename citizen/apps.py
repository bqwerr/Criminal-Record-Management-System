from django.apps import AppConfig


class CitizenConfig(AppConfig):
    name = 'citizen'

    def ready(self):
    	import citizen.signals
    	