DC=docker-compose -f docker/docker-compose.yml

.PHONY: build push mongo spiders

build:
	$(DC) build python

push:
	docker push joanfont/grissom

mongo:
	$(DC) up -d mongo

spider-%:
	$(DC) run --rm --entrypoint scrapy python runspider crawler/spiders/$*.py

spiders: spider-idealista spider-fotocasa spider-pons_oliver
