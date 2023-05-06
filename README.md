# Public Cloud

REST Backend + Asynchronous Processing Layer. Design and implementation of a scalable web application in public cloud.

This application allows compressing files using different utilities and/or algorithms: ZIP, 7Z, TAR.GZ, TAR.BZ2

## Video Explicativo
### TODO: Add video

[YouTube Link]()

## ¿Cómo desplegar la aplicación en GCP?

### Despliegue de la base de datos - Cloud SQL

En primer lugar cree una instancia de Cloud SQL en la misma región en la que creó las instancias de Compute Engine. Asegurese que utilice PostgreSQL 14.

Luego, chequee la opción de asignar IP privada, esta es la que va a utilizar para hacer llamado en la base de datos.
Verifique que la maquina pertenezca a la misma VPC que las demás maquinas desplegadas.

Luego de haber chequeado la opción, en caso de que su proyecto no tenga activadas las APIs necesarias, GCP lo redirigirá a un tutorial para activarlas y asignar correctamente esa IP privada a la VPC correspondiente.

Una vez la instancia se haya creado, reemplace la IP de la base de datos contenida en los archivos ```celery_script/tasks``` y ```__init__.py```. Solo debe reemplazar la parte contenida después del @ y antes del /.

### Despliegue del sistema de archivos de red (NFS)
### TODO: Cloud Storage

Para empezar, cree una instancia de VM utilizando Compute Engine, asegurándome que sigan las mismas especificaciones que las máquinas virtuales que representan el worker y la aplicacion.

Seguidamente, en esta instancia instalé el nfs-kernel-server que permite establecer la carpeta compartida y todas las configuraciones de esta. Para ello, cree un directorio (el que se va a compartir) y modifiqué el archivo /etc/exports/ en el cual se especifica el directorio compartido, que maquinas van a poder acceder (ips), los permisos (rw), entre otras. Por último, reinicié el este servicio.

En las VM del worker y de la app se configuraron un par de parámetros extra para realizar esta conexión. A la hora de hacer el docker.run, se debió agregar el condigo adicional “-v /mnt/nfs/cloud-conversion-tool/files:/python-docker/cloud_conversion_tool/files” que vincula la carpeta existente dentro de la instancia NFS y una carpeta de interés dentro de las instancias worker y app. De esta manera, lo que se suba en esta carpeta va ser visible y se van a poder descargar los contenidos en las demás.

### Despliegue con Docker

Puede utilizar Docker para inicializar la aplicación en GCP siguiendo las siguientes instrucciones:

En primer lugar, cree 2 instancias de VM utilizando Compute Engine y en una de ellas ejecute el worker y en la otra la aplicación. La ejecución de cada componente la podrá realizar de la siguiente forma:

#### Vincular NFS con el worker y la aplicación
### TODO: Delete NFS

En la instancia del worker y la aplicación deberá vincular el sistema de archivos de red para la escritura en el directorio compartido.

```bash
sudo mount <internal-file-server-ip>:/user-files /mnt/nfs
```

#### Ejecución del worker
### TODO: Delete NFS

```bash
sudo snap install docker
sudo docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/public-cloud-worker:main
sudo docker run --platform linux/amd64 -v /mnt/nfs/cloud-conversion-tool/files:/python-docker/cloud_conversion_tool/files ghcr.io/cloud-conversion-system/public-cloud-worker:main
```

#### Ejecución de la aplicación:
### TODO: Delete NFS

```bash
sudo snap install docker
sudo docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/public-cloud-app:main
sudo docker run --platform linux/amd64 -p 80:80 -v /mnt/nfs/cloud-conversion-tool/files:/python-docker/cloud_conversion_tool/files ghcr.io/cloud-conversion-system/public-cloud-app:main
```

### Crea una plantilla de instancias para la ejecución de la aplicación.

- Selecciona máquinas de tipo N1 f1-micro
- Disco de arranque Container-Optimized OS
- Etiqueta de red http-server para permitir conexiones por el puerto 80
- Añade lo siguiente a automatización en "secuencia de comandos de inicio":
```
#!bin/bash
sudo rm /var/credentials/google-credentials.json
sudo touch /var/credentials/google-credentials.json
echo '{
  "type": "service_account",
  "project_id": "cloud-conversion-system",
  "private_key_id": "a7a48df62c83e5d67cbbf2f4c649df0219bdd9b9",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDOqzHWxzSjOTmx\n6LjHiv0TnQIVdJ7dRxeDztIKX6UYPnihv6niBERsfG7R4xE0dn3/3CsuCqChqPvk\nbQAjU2rGfcLPol5WEZOxZeCuMR9xqTqgLOTBeI0DM1dO/vtLm2Se2p1CiBkENAzV\nYrwqf52Ee6RXDyz1DYGYRwR7Yh4S3tpbDnJyzagr0oQga3T3eFDL/lMkrJjhpJ0O\n4aQNA1OQ3UVerZZwQZlxHA1AnKNL77AijD5sng8aFh8n9NesG+lLY8+gVfkHsAT4\n2LaxjrOgRZ/N6cpDD24UOOUHBgJuc3NdX6wk2HPwDjDipxTIfjJVzvWoLZW51+UX\nSVDpU119AgMBAAECggEAFKIU3LuQrscU0oVIhWuD7sRbI+c7wR3K5Dbu02hPJEeA\nZa2r+UuxxR77NWs1GYbG95d0nCkldl5Xn6ueOuimHWEK5Q3x2yfwFeL09o8i84cQ\nulMhF4vAkFQ84D8muZqvBgkPcEgEL14+9cLgxGFvSX3Kn4J9W43YpWpZsTPPitSU\n7h7fKqp8cm1CfKBmzn0+Y0GVoCXRORiYPxqtyY5gpgubJQEklgsI10XGmJ3C5ALk\nJyGdLnCIC8/6kLtesjRuMTL2TM2kegmlg/RHftX8/3cWFjLOSahcAsAVvBdGsQmy\n8eQ/TUQvKKa7wCpMUpwf8XPURqY3VzcL93y3bZ6o5QKBgQD3KgqNX3ClaaLa6S0R\nYmlI+TtCLjFRhHY+tg8GoZFhSkR5J/NtZ4N6hloX79tZEbg20UEv6nNxJO18iqGa\nwDdkY/VtWESfEMd/nmJlXsWbZsaIs4XtdAo3qhK2Sx1Bo4w4lactwFqtXU6lcl9h\n3BeJqA5mEs7NWJscIE4P8O8rywKBgQDWDo2bOWg8Rt+I5wBHiIlXstYgCWavIQNH\nFDLyZEdUlRK+zxJdpqtOSUzwLLTJ+2Oj9rnjRbp2qXMJpOEDWE4kq0nwMy1GuiQg\ngLIzn1X0NgzSRQqY/E19qI0Qe6AG2sXlJlvCD1+r21StK0Kh8kqfijIdUUWqFGEW\nLZ0KzpoC1wKBgFbOPCCEuYJOxHSP2lU1s/Z+GfLXWFjh5cmGlWZlzjJWLBBFGLh+\n121rzC6F/gqdL46JFZTniZ3eM04/Phykj4/Bj4vUqV0YPoiyrqodi9dVVDrkmg/Y\nZlJAeAvv+5l3ACNLZAiseuxSTfHLZnZvHxEopc3xoxH5oZhSPDhbDRTbAoGBAJc8\nGwJjkeicbkyMYN8pcVfby3tBCSKMoYMzmzc0cE0rMd5L8P7nxbp/AXPjMixOh7yN\nkhIn7rDt0ZArxKqXVkaEGq4xijihROsN4lmkppbvJSnei7lA8QLp9hiCL7MIGK9o\n5YV7VS3XvcDHgsFmrSCBBB1AkYaz9VA1E/JRu/BrAoGBAMDclmcp0IQUvYjPx4Ji\nOhfynrcExjHfY4famgWlqgnzAugHBgzXF+L5oKVEtqptI0cFukJeRynNrAMVR0tG\nzyP7QwbqPuY2r4xZjWj71L7bsbECUjstvN8RB/uNyTBs0pk6Swm9bGaNA/GC1QHx\n6KggFqv1J9NhrAYlePXCOJa0\n-----END PRIVATE KEY-----\n",
  "client_email": "cloud-conversion-tool@cloud-conversion-system.iam.gserviceaccount.com",
  "client_id": "107418183991911567406",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloud-conversion-tool%40cloud-conversion-system.iam.gserviceaccount.com"
}' | sudo tee -a /var/credentials/google-credentials.json
docker pull ghcr.io/cloud-conversion-system/scalable-cloud-app:main
docker run -v /var/credentials/google-credentials.json:/python-docker/cloud_conversion_tool/credentials/google-credentials.json -p 80:80  ghcr.io/cloud-conversion-system/scalable-cloud-app:main
```

```
#!bin/bash
sudo rm /var/credentials/google-credentials.json
sudo touch /var/credentials/google-credentials.json
echo '<CREDENTIALS_JSON>' | sudo tee -a /var/credentials/google-credentials.json
docker pull ghcr.io/cloud-conversion-system/scalable-cloud-app-worker:main
docker run -v /var/credentials/google-credentials.json:/python-docker/cloud_conversion_tool/credentials/google-credentials.json -p 80:80  ghcr.io/cloud-conversion-system/scalable-cloud-app-worker:main
```
- Habilitar monitoring y logging

## Documentación del API

[Postman Documentation](https://documenter.getpostman.com/view/11708390/2s93Y5NeWB)

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](LICENSE)**
- Copyright 2023 © Cloud Conversion System
