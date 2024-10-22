# BookstoreRestAPI
Examen segundo parcial - Alonso Gutiérrez Varela - Sistemas Distribuidos


# LibreriaAPI

Este proyecto es una API para gestionar una librería, incluyendo funcionalidades como buscar libros por título, gestionar autores y más. Utiliza **Flask** como framework web y **MongoDB** como base de datos.

## Requisitos previos

Asegúrate de tener instalados los siguientes programas antes de continuar:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Instrucciones de instalación

### 1. Clonar el repositorio

Para obtener una copia local del proyecto, ejecuta el siguiente comando en tu terminal:

```
git clone https://github.com/AlonsoGtzV/BookstoreRestAPI
```

Luego navega al directorio del proyecto:

```
cd BookstoreRestAPI
```

### 2. Configuración del entorno

Asegúrate de tener un archivo `.env` en la raíz del proyecto. Si no lo tienes, crea uno con las siguientes variables:

```
FLASK_APP=app.py
FLASK_ENV=development
MONGO_URI=mongodb://mongo:27017/libreriaDB
```

Esto configurará la aplicación para utilizar Flask en modo de desarrollo y conectarse a la base de datos MongoDB a través de Docker.

### 3. Ejecutar los contenedores

Usaremos Docker y Docker Compose para correr tanto la API como la base de datos MongoDB en contenedores. Si ya tienes Docker Compose configurado, solo necesitas ejecutar el siguiente comando:

```
docker-compose up --build
```

Esto hará lo siguiente:
- **Construirá la imagen Docker** de la API.
- **Ejecutará los contenedores** tanto para la API como para MongoDB.

### 4. Verificar que la API esté corriendo

Una vez que Docker haya terminado de levantar los contenedores, la API debería estar accesible en:

```
http://localhost:5000
```

Puedes verificar si está corriendo correctamente haciendo una solicitud GET a la siguiente ruta, por ejemplo:

```
curl http://localhost:5000/book/title/<nombre-del-libro>
```

### 5. Administración de la base de datos MongoDB

MongoDB estará corriendo en el puerto `27017` dentro del contenedor, pero puedes conectarte desde tu máquina local usando un cliente como [MongoDB Compass](https://www.mongodb.com/products/compass) o la terminal con la siguiente URI:

```
mongodb://localhost:27017
```

### 6. Parar los contenedores

Cuando termines de usar la API y MongoDB, puedes parar y eliminar los contenedores con el siguiente comando:

```bash
docker-compose down
```

Este comando detiene los contenedores sin eliminar las imágenes.

## Configuración adicional

- Si necesitas cambiar el puerto donde corre la API o MongoDB, puedes hacerlo modificando el archivo `docker-compose.yml`.
- Para agregar nuevos módulos o bibliotecas a la API, edita el archivo `requirements.txt` y luego reconstruye la imagen con:

```bash
docker-compose up --build
```

Para probar la API puedes utilizar swagger-ui, que se encuentra en http://localhost:5000/swagger-ui
