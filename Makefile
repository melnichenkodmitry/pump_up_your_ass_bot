PROJECT_NAME = pump_up_your_ass
VERSION = 1.0

up_dockerfile:
	docker run --name $(PROJECT_NAME) -v .:/home/pump_up_your_ass --rm --network pump_up_your_ass_network -p 8010:8010 $(PROJECT_NAME):$(VERSION)
up:
	docker compose up
build:
	docker build . -t $(PROJECT_NAME):$(VERSION)
push:
	docker push