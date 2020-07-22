DC=docker-compose -f docker/docker-compose.yml

build:
	$(DC) build python

push:
	docker push joanfont/grissom

mongo:
	$(DC) up -d mongo

spider-%:
	$(DC) run --rm --entrypoint scrapy python runspider $*
