# Yonesto Django Application

Este proyecto es una aplicación Django contenida en Docker. Para facilitar el proceso de construcción y ejecución, se proporciona un `Makefile`.

## Prerrequisitos:

- **Docker**: Debe estar instalado en tu máquina.




## Uso del Makefile:

El `Makefile` facilita varias tareas comunes al trabajar con Docker:


```bash
make build
```

### 1. Construir la imagen de Docker:

Para construir la imagen Docker a partir del Dockerfile proporcionado:



```bash
make run
```

### 2. Ejecutar la aplicación:

Para construir (si no se ha hecho previamente) y ejecutar la aplicación Django en un contenedor:

Esto correrá tu aplicación y la expondrá en el puerto `8000`.



```bash
make stop
```

### 3. Detener la aplicación:

Para detener y eliminar el contenedor de la aplicación:



```bash
make restart
```

### 4. Reiniciar la aplicación:

Si necesitas hacer cambios y reiniciar la aplicación, puedes utilizar:



Esto detendrá el contenedor actual, reconstruirá la imagen y luego iniciará un nuevo contenedor con la imagen actualizada.

## Contribución:

Cualquier contribución al proyecto es bienvenida. Asegúrate de seguir las mejores prácticas al trabajar con Django y Docker.

## Licencia:

[Nombre de la licencia, por ejemplo: MIT]
