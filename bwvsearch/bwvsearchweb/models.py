from django.db import models
from elasticsearch import Elasticsearch
from music21 import *

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
            score.key = hit['_source']['key']
            score.score = hit['_score']
            hits.append(score)
        return hits


# Create your models here.
class Score(models.Model):
    name = models.CharField(max_length=200)
    key = models.CharField(max_length=200)
    score = models.FloatField()
    objects = ScoreManager()

    class Meta:
        managed = False