from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
from django.db import models
from elasticsearch import Elasticsearch
from music21 import *
import os

class ScoreManager(models.Manager):
    _es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    
    def with_pitched_chords(self, chords):
        res = self._es.search(
            index="score-chords-index",
            body={
                "query": {
                    "match_phrase": {
                        "chords": chords
                    }
                }
            }
        )
        hits = []
        for hit in res['hits']['hits']:
            score = Score()
            score.name = hit['_source']['name']
            score.date = hit['_source']['date']
            score.file_path = hit['_source']['filePath']
            score.key = hit['_source']['key']
            score.score = hit['_score']
            hits.append(score)
        return hits


# Create your models here.
class Score(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    file_path = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    score = models.FloatField()
    objects = ScoreManager()

    @property
    def image(self):
        filename = ''
        if (not default_storage.exists(self.file_path.replace('/', '_') + '.png')):
            environment.set('directoryScratch', settings.MEDIA_ROOT)
            environment.set('musescoreDirectPNGPath', '/vagrant/sh/mscore.sh')
            environment.set('musicxmlPath', '/vagrant/sh/mscore.sh')
            path = corpus.parse(self.file_path).write('musicxml.png')
            os.rename(path, settings.MEDIA_ROOT + self.file_path.replace('/', '_') + '.png')
        return default_storage.url(self.file_path.replace('/', '_') + '.png')

    class Meta:
        managed = False