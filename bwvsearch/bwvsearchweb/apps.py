from django.apps import AppConfig
from music21 import environment
from django.conf import settings


class BwvsearchwebConfig(AppConfig):
    name = 'bwvsearchweb'

    def ready(self):
        environment.set('directoryScratch', settings.MEDIA_ROOT)
        environment.set('musescoreDirectPNGPath', settings.BASE_DIR + '/sh/mscore.sh')
        environment.set('musicxmlPath', settings.BASE_DIR + '/sh/mscore.sh')
