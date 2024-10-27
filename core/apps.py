from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    name = 'core'

class SeuAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sgeme'  # Deve ser o mesmo nome da pasta do seu aplicativo
