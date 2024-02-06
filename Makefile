IMAGE_NAME := django-app-image
CONTAINER_NAME := django-app-container
PORT := 8000

# Targets
# all: build run

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -p $(PORT):$(PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)

clean: stop
	docker rm $(CONTAINER_NAME)
	docker rmi $(IMAGE_NAME)

.PHONY: build run stop clean