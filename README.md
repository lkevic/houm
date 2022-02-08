# Houm

---

##  Backend Tech Lead Challenge

### Problema

En Houm tenemos un gran equipo de Houmers que muestran las propiedades y solucionan
todos los problemas que podrían ocurrir en ellas. Ellos son parte fundamental de nuestra
operación y de la experiencia que tienen nuestros clientes. Es por esta razón que
queremos incorporar ciertas métricas para monitorear cómo operan, mejorar la calidad de
servicio y para asegurar la seguridad de nuestros Houmers.

### Requisitos

Crear un servicio REST que:

* **Punto 1:** Permita que la aplicación móvil mande las coordenadas del Houmer
* **Punto 2:** Para un día retorne todas las coordenadas de las propiedades que visitó y cuanto
tiempo se quedó en cada una
* **Punto 3:** Para un día retorne todos los momentos en que el houmer se trasladó con una
velocidad superior a cierto parámetro

## Solución

La solución consta de un servicio REST desarrollado en Python que utiliza Django
como framework base. Adicionalmente, implementa Django Rest Framework y 
Django OAuth Toolkit.

El servicio cuenta con un esquema de seguridad basado en roles y utiliza el 
protocolo OAuth2 para la autenticación tanto de los usuarios como de las 
aplicaciones cliente. Todos los usuarios (Houmers) activos del sistema pueden 
reportar su ubicación (coordenadas). Pero, solo los usuarios con rol de 
administración pueden consultar los reportes sobre otros usuarios y gestionar 
las propiedades.

El servicio expone endpoints para autenticación, reportar ubicación, extraer 
reporte de visitas a propiedades, extraer reporte de movimiento y gestionar 
las propiedades cargadas en el sistema. Adicionalmente, expone un endpoint
para verificar el estado del servicio y un módulo de documentación online
(Swagger) solo para entornos de desarrollo.

### Consideraciones y aclaraciones

#### Generales

* Se adopta cálculo de distancias geodésica sobre el modelo elipsoidal WGS-84.
* Las coordenadas (latitud y longitud) están representadas en grados decimales. 
* Las alturas están representadas en metros. 

#### Punto 1

* La aplicación móvil debe reportar latitud, longitud, altura y fecha de dichas coordenadas.
* Se asume que los datos reportados tienen la suficiente periodicidad y precisión como para que los cálculos sean coherentes. 

#### Punto 2

* Las propiedades debe estar cargadas en el servicio. El servicio expone enpoints (listar, ver, crear, modificar y eliminar propiedades) para que los usuarios con rol de administración puedan gestionar dichos datos.
* Se asume que el usuario que carga las propiedades conoce las coordenadas centrales de las propiedades y sus tamaños.
* Las propiedades están representadas por coordenadas (centrales) y un *radio de tolerancia*. Cualquier par de coordenadas que se encuentre a una distancia menor al *radio de tolerancia* de las coordenadas centrales de la propiedad, serán consideradas interiores a la propiedad.
* Se considera que un Houmer está en una propiedad si sus coordenadas son interiores a una propiedad.
* Si varias propiedades tienen zonas internas compartidas (intersección) y un Houmer se encuentra en una de esas zonas, el servicio devolverá la primera propiedad que encuentre.
* Se considera el tiempo de permanencia desde el primer reporte dentro de la propiedad hasta el último reporte dentro de la propiedad. Si existe un solo reporte dentro de los límites de la propiedad el tiempo de permanencia será 0.
* El reporte tiene en cuenta locaciones con más de 30 segundos de diferencia. Las locaciones con menos de 30 segundos serán descartadas para este reporte. De manera que la precisión del reporte será de +- 30 segundos.  

#### Punto 3

* La velocidad se expresa en Kilómetros por hora.
* Para el cálculo de velocidad se tiene en cuenta el desplazamiento sobre la longitud, la latitud y la altura.
* El reporte tiene en cuenta locaciones con más de 30 segundos de diferencia. Las locaciones con menos de 30 segundos serán descartadas para este reporte. De manera qeu la precisión del reporte será de +- 30 segundos.

## Requerimientos

* Python 3.8+

## Backing services

El servicio opera con una base de datos SQL. Se puede utilizar SQLite para 
desarrollo y pruebas. Pero, es altamente recomendable utilizar un motor de
base de datos más robusto en entornos productivos (como PostgreSQL).

## Primeros pasos

En esta sección se explica como ejecutar el servicio utilizando Virutalenv.

Si prefiere ejecutar la solución con docker sobre su entorno local vea 
[Docker para desarrollo](#docker-para-desarrollo)

### Configuración del entorno de desarrollo

#### 1. Crear y activar un entorno virtual

Crear y activar el entorno virutual con Virtualenv. Este paso no es necesario,
pero si es recomendable en entornos de desarrollo.

En el directorio raíz de la aplicación ejecutar los siguientes comandos. 

Crear el entorno virtual:

```shell
python3 -m venv env  
```

Activar el entorno virtual:

```shell
source env/bin/activate  
```

En Windows se debe utilizar `env\Scripts\activate`.

#### 2. Instalar todas las dependencias

Instalar todas las dependencias del proyecto.

```shell
pip install -r requirements.txt 
```

#### 3. Sincronizar la base de datos por primera vez

Sincronizar base de datos.

```shell
python manage.py migrate
```

Con la configuración por defecto se creará una base de datos DQLite en el 
directorio raíz de la aplicación. Esto es solo con fines de desarrollo, no
se debe utilizar la configuración por defecto en entornos de producción.

#### 4. Crear aplicación cliente (OAuth2)

Para realizar la autenticación contra el servicio es necesario crear una 
aplicación cliente (OAuth2).
En este ejemplo se creará un cliente con client_type confidential y grant_type
password.

```shell
python manage.py createapplication --client-id <your-client-id> --client-secret <your-client-secret> --name <your-client-name> confidential password
```

Otros tipos de clientes pueden ser generados. Pero por el momento el servicio
no expone páginas para autenticación online. Ejecute 
`python manage.py createapplication -h` para más detalles.

#### 5. Crear el primer usuario

Para crear un usuario activo con permisos de administración, se debe ejecutar
el siguiente comando.

```shell
 python manage.py createhoumeruser --user <username> --password <password> --admin True 
```

### Probando el servicio

#### Iniciar el servidor de desarrollo

Iniciar el servicio en nuestro entorno de desarrollo.

```shell
python manage.py runserver
```

Si todo salió bien veremos la siguiente salida en la consola.

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 07, 2022 - 23:39:56
Django version 4.0.2, using settings 'core.settings.develop'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Ahora el servidor ya se encuentra en ejecución.

Puede visitar la siguiente URL para verificar su funcionamiento 
http://127.0.0.1:8000/docs/swagger/

#### Obtener el token del usuario

Primero necesitamos obtener un token válido para nuestro usuario. 
Utilizaremos las credenciales generales en los pasos 4 y 5 de 
[Configuración del entorno de desarrollo](#configuración-del-entorno-de-desarrollo) .

```shell
curl --location --request POST 'http://127.0.0.1:8000/auth/token/' \
--header 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=password' \
--data-urlencode 'client_id=<your-client-id>' \
--data-urlencode 'client_secret=<your-client-secret>' \
--data-urlencode 'username=<username>' \
--data-urlencode 'password=<user-password>'
```

Obtendremos un resultado como el siguiente.

```json
{
  "access_token": "<access-token>", 
  "expires_in": 36000, 
  "token_type": "Bearer", 
  "scope": "read write", 
  "refresh_token": "<refresh-token>"
}
```

#### Obtener el estado del servicio

Obtendremos el estado de nuestro servicio con un GET en el endpoint de estado. 
Utilizaremos para esto el token obtenido en el paso anterior.

```shell
curl --location --request GET 'http://127.0.0.1:8000/api/v1/status' \
--header 'Authorization: Bearer <access-token>'
```

Obtendremos un resultado como el siguiente.

```json
{
  "service":"Houmers",
  "status":"Ok"
}
```

## API Docs

Con la configuración en modo desarrollo (default), el servicio expone documentación
online en la siguiente url (Swagger):

* /docs/swagger/

La GUI de Swagger puede ser utilizada para probar los endpoints. Incluye una
funcionalidad que permite autenticarse con el servicio.

## Authentication

El servicio expone los siguientes endpoints del protocolo OAuth 2.

* **Authorize endpoint:** /auth/authorize/
* **Token endpoint:** /auth/token/
* **Revoke token endpoint:** /auth/revoke_token/
* **Introspect endpoint:** /auth/introspect/

### Crear una aplicación cliente

Para crear una aplicación cliente se debe ejecutar el siguiente comando.

```shell
python manage.py createapplication --client-id <your-client-id> --client-secret <your-client-secret> --name <your-client-name> confidential password
```

Este cliente puede ser utilizado para la GUI e Swagger.

### Crear y modificar usuarios

Los usuarios se gestionan desde la consola.  

Crear un usuario administrador:

```shell
 python manage.py createhoumeruser --user <username> --password <password> --admin True
```

Crear un usuario no administrador:

```shell
 python manage.py createhoumeruser --user <username> --password <password> --admin False 
```

Modificar un usuario:

```shell
 python manage.py updatehoumeruser --user <username> --newpassword <password> --active True --admin False 
```

Ejecute `python manage.py createhoumeruser --help`  y `python manage.py updatehoumeruser --help`
para más información.

## Settings

El servicio es configurado mediante variables de entorno.

### Variables de entorno

* **DJANGO_SETTINGS_MODULE**: Django Settings Module. 
  * **core.settings.develop**: (default) Entorno de desarrollo.
  * **core.settings.test**: Para pruebas unitarias.
  * **core.settings.production**: Para entornos productivos.
* **SECRET_KEY**: Django SECRET_KEY. Tiene que ser larga y secreta. Para más información vea https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-SECRET_KEY
* **DATABASE_URL**: SQL database URI.

## Ejecutar test unitarios

Para ejecutar los tests unitarios de la aplicación se debe configurar la variable
de entorno DJANGO_SETTINGS_MODULE con el valor core.settings.test y luego utilizar
la herramienta de pruebas de Django.

```shell
export DJANGO_SETTINGS_MODULE="core.settings.test"
python manage.py test
```

## Docker para desarrollo

Es posible utilizar Docker Compose para ejecutar la solución en un entorno de
desarrollo (o local). 

A continuación se enumeran los pasos para la ejecución con Docker Compose.

### 1. Crear y levantar el servicio

Sobre el directorio raíz de la aplicación ejecutar el siguiente comando. 

```shell
docker-compose up --build
```

Esto iniciará dos servicios "web" (API) y "db" (Postgres DB)

Puede utilizar otra instancia de consola para los siguientes pasos.
Siempre sobre el directorio raíz de la aplicación.

### 2. Actualizar el esquema de base de datos

Ejecutar el siguiente comando para actualizar el esquema de la base de datos
PostgreSQL.

```shell
docker-compose run web python manage.py migrate
```

### 3. Crear la aplicación cliente de 0Auth 2

Para crear una aplicación cliente se debe ejecutar el siguiente comando.

```shell
docker-compose run web python manage.py createapplication --client-id <your-client-id> --client-secret <your-client-secret> --name <your-client-name> confidential password
```
 
### 4. Crear el primer usuario

Para crear un usuario activo con permisos de administración, se debe ejecutar
el siguiente comando.

```shell
docker-compose run web python manage.py createhoumeruser --user <username> --password <password> --admin True
```

Ahora el servidor está en ejecución y ya contamos con las credenciales necesarias
para operar. 

Ingresando a http://0.0.0.0:8000/docs/swagger/ desde nuestro navegador 
visualizaremos la documentación online (Swagger) y podremos realizar pruebas 
(utilizando las credenciales que hemos generado).
