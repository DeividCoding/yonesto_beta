IMAGE_NAME=yonesto_django_app
PORT=9595

# Construir la imagen de Docker
build:
	@docker build -t $(IMAGE_NAME) .

# Correr la aplicación Django en un contenedor
# @docker run -d -p $(PORT):8000 --name $(IMAGE_NAME)_container $(IMAGE_NAME)
run: build
	@docker run  -p $(PORT):8000 --name $(IMAGE_NAME)_container $(IMAGE_NAME)
	
# Detener y eliminar el contenedor
stop:
	@docker rm -f $(IMAGE_NAME)_container || true

# Reiniciar la aplicación (reconstruir la imagen y reiniciar el contenedor)
restart: stop run

.PHONY: build run stop restart
