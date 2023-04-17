# Traditional Environment

REST Backend + Asynchronous Processing Layer. Scalable web applications in a traditional environment.

This application allows compressing files using different utilities and/or algorithms: ZIP, 7Z, TAR.GZ, TAR.BZ2

## Video Explicativo

[YouTube Link](https://youtu.be/ej0_3Xr8v3E)

## ¿Cómo desplegar la aplicación?

Requerimientos:
* Tener una máquina Linux en donde pueda desplegar un broker de Redis.
* Tener el repositorio clonado en la maquina en donde va a desplegar el servidor.
* Debe tener Python3 instalado en la maquina en donde va a desplegar el servidor.
* Debe tener acceso disponible a la instancia RDS de AWS que maneja la base de datos.

1. Instale las librerias necesarias con el archivo requeriments.txt, para esto ejecute el siguiente comando en su consola.
```pip install -r requirements.txt```
2. Instale redis y despliegue el servidor, para esto debe seguir los siguientes pasos:
2.1. Ejecute los siguientes comandos en su consola:
```sudo apt-get install redis-server```
```sudo systemctl enable redis-server.service```
```redis-server```
3. Dirigase al directorio del proyecto y digite los siguientes comandos en consola:
```celery -A cloud_conversion_tool.celery_script worker -l info```
1. Ejecute el servidor de Flask en otra consola.

### Despliegue con Docker

Alternativamente, puede utilizar Docker para inicializar la aplicación con los siguientes comandos:

1. `docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/traditional-environment:main`
2. `docker run --platform linux/amd64 -p 80:80 -i ghcr.io/cloud-conversion-system/traditional-environment:main`

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](LICENSE)**
- Copyright 2023 © Cloud Conversion System
