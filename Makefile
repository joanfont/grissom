build:
	docker build -t joanfont/grissom .

push:
	docker push joanfont/grissom

mongo:
	docker-compose up -d mongo