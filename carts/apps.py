from django.apps import AppConfig


class CartsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'carts'

    def ready(self):
        import carts.signals #This ensures Django loads your signals when the app starts
