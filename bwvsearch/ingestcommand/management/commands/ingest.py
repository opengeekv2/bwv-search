from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch
from music21 import *

class Command(BaseCommand):
    help = 'Feeds Elasticsearch with Bach Chorales'

    def connect_elasticsearch(self):
        _es = None
        _es = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])
        if _es.ping():
            print('Yay Connect')
        else:
            print('Awww it could not connect!')
        return _es

    def create_index(self, es_object, index_name="score-chords-index"):
        created = False
        # index settings
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "score-chords": {
                    "dynamic": "dynamic",
                    "properties": {
                        "name": {
                            "type": "text"
                        },
                        "filePath": {
                            "type": "text"
                        },
                        "key": {
                            "type": "text"
                        },
                        "chords": {
                            "type": "text"
                        }
                    }
                }
            }
        }
        try:
            if not es_object.indices.exists(index_name):
                # Ignore 400 means to ignore "Index Already Exist" error.
                es_object.indices.create(index=index_name, ignore=400, body=settings)
                print('Created Index')
            created = True
        except Exception as ex:
            print(str(ex))
        finally:
            return created

    def generateScoreChordIndex(self, chorale):
        flatChorale = chorale.flat.notes
        choraleChordify = flatChorale.chordify().notes
        chords = ''
        for chord in choraleChordify:
            chords = chords + ' ' + chord.pitchedCommonName
        return {
            'name': chorale.metadata.title,
            'filePath': chorale.corpusFilepath,
            'key': chorale.analyze('key').tonicPitchNameWithCase,
            'chords': chords
        }

    def putChordIndex(self, es, id, scoreChords):
        res = es.index(index="score-chords-index", doc_type='score-chords', id=id, body=scoreChords)
        print(res['result'])

    def handle(self, *args, **options):
        es = self.connect_elasticsearch()
        self.create_index(es, "score-chords-index")
        try:
            i = 0
            for chorale in corpus.chorales.Iterator():
                scoreChords = self.generateScoreChordIndex(chorale)
                self.putChordIndex(es, i, scoreChords)
                i = i + 1
        except corpus.chorales.BachException:
            pass
        es.indices.refresh(index="score-chords-index")
        res = es.search(index="score-chords-index", body={"query": {"match_all": {}}})
        print("Got %d Hits:" % res['hits']['total'])
        

