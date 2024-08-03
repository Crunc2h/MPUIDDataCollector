from django.apps import AppConfig


class InternalReprConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'internal_repr'
