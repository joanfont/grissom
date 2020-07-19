build:
	docker build -t joanfont/grissom .

push:
	docker push joanfont/grissom

mongo:
	docker-compose up -d mongo

run-spider:
	docker-compose run --rm --entrypoint scrapy python runspider $1
