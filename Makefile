up:
	docker-compose -f -d "docker-compose.yml" up

provision:
	docker-compose -f -d "docker-compose.yml" up --build

ingest:
	docker-compose run bwv-ingest

test:
	docker exec -it bwv-search_bwv-search_1 python manage.py test

update:
	cp requirements.txt bwvsearch/requirements.txt
	docker exec -it bwv-search_bwv-search_1 pip install -r requirements.txt
	docker exec -it bwv-search_bwv-search_1 /bin/bash -c "pip freeze > requirements.lock.txt"
	mv bwvsearch/requirements.lock.txt requirements.lock.txt

install: requirements.lock.txt
	cp requirements.lock.txt bwvsearch/requirements.lock.txt
	docker exec -it bwv-search_bwv-search_1 pip install -r requirements.lock.txt
	rm bwvsearch/requirements.lock.txt