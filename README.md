# Guía de Configuración y Ejecución de Aplicación Python con Tornado y MySQL

## Descripción de la Arquitectura

Esta aplicación utiliza Python con el framework Tornado para manejar solicitudes HTTP y comunicarse con una base de datos MySQL. La base de datos se ejecuta en un contenedor Docker, proporcionando un entorno de base de datos consistente y fácil de configurar. El código de la aplicación y la configuración de la base de datos están alojados en GitHub, permitiendo una fácil distribución y despliegue.

La estructura del proyecto es la siguiente:

-   `/app/app.py`: Contiene el código fuente de la aplicación Python con Tornado.
-   `/mysql/docker-compose.yaml`: Define la configuración del contenedor Docker para MySQL.

## Pre-requisitos

Asegúrate de tener instalado lo siguiente en tu entorno Windows:

-   Git
-   Python 3.x
-   pip (Administrador de paquetes de Python)
-   Docker Desktop para Windows

## Paso 1: Clonar el Repositorio

Clona el repositorio desde GitHub para obtener el código de la aplicación y la configuración de Docker. Abre una terminal y ejecuta:

bashCopy code

`git clone https://github.com/Edunzz/python_tornado_sqlalchemy.git
cd python_tornado_sqlalchemy` 

## Paso 2: Instalación de Bibliotecas Python

Instala las bibliotecas necesarias para Python utilizando pip. En la terminal, ejecuta:

bashCopy code

`pip install tornado sqlalchemy pymysql` 

## Paso 3: Definición de Variables de Entorno

Define las variables de entorno necesarias en Windows:

1.  Abre el Panel de Control.
2.  Navega a Sistema y Seguridad > Sistema.
3.  Haz clic en "Configuración avanzada del sistema".
4.  En Propiedades del Sistema, selecciona "Variables de Entorno".
5.  Agrega las siguientes variables:
    -   `DBHOST`: La dirección IP del contenedor Docker de MySQL.
    -   `DBPORT`: El puerto de acceso a MySQL (usualmente 3306).

## Paso 4: Levantar el Contenedor Docker MySQL

En la terminal, navega a la carpeta `/mysql` y ejecuta:

bashCopy code

`docker-compose up -d` 

Esto levantará el contenedor de MySQL según la configuración definida en `docker-compose.yaml`.

## Paso 5: Obtener la IP del Contenedor Docker

Para obtener la dirección IP del contenedor, utiliza:

bashCopy code

`docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' nombre_contenedor` 

Reemplaza `nombre_contenedor` con el nombre real de tu contenedor MySQL.

## Paso 6: Ejecutar la Aplicación Python

Navega a la carpeta `/app` y ejecuta el script `app.py`:

bashCopy code

`python app.py` 

## Conclusión

Al seguir estos pasos, tendrás tu aplicación Python con Tornado corriendo y conectándose a una base de datos MySQL en un contenedor Docker en Windows.
