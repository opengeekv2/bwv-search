from django.db import models
from elasticsearch import Elasticsearch
from music21 import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings

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
            score.image = default_storage.save('/' + score.file_path + '.png', ContentFile(corpus.parse(score.file_path).write('lily.png')))
            hits.append(score)
        return hits


# Create your models here.
class Score(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    file_path = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    score = models.FloatField()
    image = models.ImageField(upload_to=settings.MEDIA_ROOT + 'scores')
    objects = ScoreManager()

    class Meta:
        managed = False