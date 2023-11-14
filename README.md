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

    git clone https://github.com/Edunzz/python_tornado_sqlalchemy.git
    cd python_tornado_sqlalchemy

## Paso 2: Instalación de Bibliotecas Python

Instala las bibliotecas necesarias para Python utilizando pip. En la terminal, ejecuta:

    pip install tornado sqlalchemy pymysql

Instala las bibliotecas necesarias para Otel Python utilizando pip. En la terminal, ejecuta:

    pip install opentelemetry-api
    pip install opentelemetry-sdk
    pip install opentelemetry-instrumentation
    pip install opentelemetry-instrumentation-tornado
    pip install opentelemetry-exporter-otlp

## Paso 3: Levantar el Contenedor Docker MySQL
En la terminal, navega a la carpeta `/mysql` y ejecuta:

    docker-compose up -d
    docker ps -a

Esto levantará el contenedor de MySQL según la configuración definida en `docker-compose.yaml`.

## Paso 4: Obtener la IP del Contenedor Docker
Para obtener la dirección IP del contenedor, utiliza:

    docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysqldb
Nota: Si el contenedor esta en vm usar la ip de la vm con el puerto 3306 de la bd.

## Paso 5: Definición de Variables de Entorno
Para configurar las variables de entorno necesarias para la aplicación, puedes utilizar la consola de comandos (CMD) en Windows. Es importante que uses la misma instancia de CMD para configurar las variables y para ejecutar tu aplicación, ya que las variables de entorno establecidas en CMD son específicas de esa sesión.

3.1.  **Abrir CMD en la Ruta Correcta:**
Presiona `Win + R`, escribe `cmd` y presiona `Enter`.
Navega a la carpeta donde clonaste el repositorio utilizando el comando `cd`. Por ejemplo:

    cd ruta\a\python_tornado_sqlalchemy
        
3.2.  **Establecer Variables de Entorno:**
En la ventana de CMD, establece las variables de entorno utilizando el comando `set`. Por ejemplo:
                
    set DBHOST=la_ip_de_tu_contenedor
    set DBPORT=3306

Para la instrumentación OTEL api dynatrace se requiere tenat url y el token:
                
    set DT_URL={url del tenant ej: https://{your-environment-id}.live.dynatrace.com/api/v2/otlp/v1/traces }
    set DT_TOKEN={token con los permisos: ingesting traces, logs, and metrics}

Nota: Para mayor detalle pueden consultar [otlpexport](https://docs.dynatrace.com/docs/shortlink/otel-getstarted-otlpexport#export-to-activegate) [authentication](https://docs.dynatrace.com/docs/shortlink/otel-getstarted-otlpexport#authentication-export-to-activegate)

3.3.  **Verificar Variables de Entorno:**
Puedes verificar que las variables se hayan establecido correctamente con:
                
    echo %DBHOST%
    echo %DBPORT%
        
Deberías ver los valores que acabas de establecer.
3.4.  **Mantener Abierta la Consola de Comandos:**
Mantén abierta esta ventana de CMD para ejecutar tu aplicación Python. Si cierras esta ventana o abres una nueva, tendrás que volver a establecer las variables de entorno.

## Paso 6: Ejecutar la Aplicación Python
Navega a la carpeta `/app` y ejecuta el script `app.py`:

    cd app
    python app.py

### Opciones de instrumentación para python con dynatrace
instrumentación open telemetry con exporters a apis dynatrace

    python app_otel.py

instrumentación open source con sdk dynatrace y one agent

    python app_autodynatrace.py

instumentación dynatrace sdk

    python app_sdk.py

## Prueba
### GET a `/ping`
Para hacer un `GET` a la ruta `/ping`, abre tu línea de comandos o cmd y ejecuta:

    curl http://localhost:8888/ping

### POST con un Número (5798)
Para realizar un `POST` a la ruta `/pedido` con un número (en este caso, 5798), abre tu línea de comandos o cmd y ejecuta:

    curl -X POST http://localhost:8888/pedido -H "Content-Type: application/json" -d "{\"numero\": 5798}"

### GET a `/pedidos`
Para hacer un `GET` a la ruta `/pedidos`, abre tu línea de comandos o cmd y ejecuta:

    curl http://localhost:8888/pedidos

## Conclusión
Al seguir estos pasos, tendrás tu aplicación Python con Tornado corriendo y conectándose a una base de datos MySQL en un contenedor Docker en Windows.
