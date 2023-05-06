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
  "private_key_id": "230008594b13114d489ee3c30f9571f289511c08",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCm/rU/v5CA1jqX\nVVw97gcI+9H0RUQvabvyGz8GNN2AtTUV5vfKgzwOdJDoXQAep4xE4BI+EFiqcCcA\nzwn/gR0hwQUalDzWPdGp9WTOepTyTmX2GhJVK45cheHjYoNPhs62z+9xGFPXREW+\nhbnBpxu1DQ5owm6HudeDB3vvjUiWocVu5jd42gc7A60+SgwOZfEqI5fc3hu+91yn\nfUHLDujoIue512dteml1iiO+J1XbJ34fu8l8dFzAWT4E5uFAxoJ3wDEDQ5ol5D9c\nYaQ86HNTXDJo+/AxjWo6loNqqhrzlrIS3rb3qx+Y++iD/1X3urnAlMmsh3bZxXJn\n+HXoE2dtAgMBAAECggEADXa4CUGPdnu53Jf9aGF9AAyW2FwPS8f5Zw3Vo9FLpy60\n7s+g3HB+kpHJBHBJwVmegF0VIMYznTDj9szlJaGfcNMS7299L4QWF98DjMwq9Gro\nDef7NhJdbM3p25SGjrkJMzRfkzLewO/YXwHWwKtm8KQdVx/km8fFfY3IaxTCgfZm\nW42butKByvgimnzHT27oKHxEHmxWXbHdcBt5CCAz81E+cyqppNgZFl9ns9kyb0Xm\nGcZvGP94ZneBBlyqPK2b7fHDb3may8/hOvX3WgsRkZ92zUOP9T+1mQq1C4ODfYkc\n7smSZJFZvesX3OaqvTnaIk31AbpwzhEMeHt04h74oQKBgQDsEVX32HxaRzoI15zf\nHl1EW2PZVM2hy5wHoSRNWiT+YNzv7QeTurDDsBq7U/BLCT+QGAlpIIlDceDoGu5T\ndpmsoOo7rryiIVWvgtItza6VELWFuTZI1qHSNtoM+HIe4WuUt5bzqzUzPzXFPjk4\nD5hzWAMESzLck9dGhYojghCkvQKBgQC1GFjAe1COafvwADgdYhLq7vKOClTdfzpU\n20exI8MtSoQdrxcvtDisXJ9tCaKs91+r1NCbahg8Enxlz9r8l/sMTVen5WPKDyq6\ntAbPs9nNn/B3kQ/DTbnNlGZzxU6aNVRteRGOHD3Ns4j02ZenpXRjSwTOyV7hY4xb\nmQyjP8hwcQKBgD9LlqVRomYCWwkr5p/cYF2Hs4n+NvR+x2M0Tat/1BNwnUynXTS7\nBdIyUbiQlQlJfYWBLGTHmIZA7nDNZ8FxN1sV+jfubh16mqLojLpDP+AwDrvAIVH+\nWn0mv+hiZRbqkhHZ99t1uFn5RM2SFX12kQW8P3LTRtvlt/7sp1FF+nhxAoGAFUhV\nNdnIL9R4zU3ZSmq6Om32h4bjTlyjaFGU7VZ8m5gEStDG8s5FUsxX2CKnwZgY4ELU\neU9Qpc6uW/C/lavuzxVP1eV5gsehh+ucWVCTqjy/r+2WYqeBzI1CNRzdDfZyg6MU\n0xSylrggwlXIIuWo9fpdCEhWJDrkxecIuy7FyaECgYEAjpCLSDhip1YXjz4d18/2\nI8DNLfrEdGB7Gk+HiTV6oLnBeN3a7BNv9IRDhx/jhjuJHOxcD/m0CUWSwuLddamq\nx6M2dwWN9kI8RCWl9sfnmRoWCeJT8zHeX23OBYR2cd0Vpz0bloPZpg91Hbe1ygbx\nwrV4oa8fu2FBkjcIW/ZdqxM=\n-----END PRIVATE KEY-----\n",
  "client_email": "cloud-conversion-tool@cloud-conversion-system.iam.gserviceaccount.com",
  "client_id": "107418183991911567406",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cloud-conversion-tool%40cloud-conversion-system.iam.gserviceaccount.com"
}
' | sudo tee -a /var/credentials/google-credentials.json
docker pull ghcr.io/cloud-conversion-system/scalable-cloud-app:main
docker run -v /var/credentials/google-credentials.json:/python-docker/cloud_conversion_tool/credentials/google-credentials.json -p 80:80  ghcr.io/cloud-conversion-system/scalable-cloud-app:main
```

```
```
- Habilitar monitoring y logging

## Documentación del API

[Postman Documentation](https://documenter.getpostman.com/view/11708390/2s93Y5NeWB)

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](LICENSE)**
- Copyright 2023 © Cloud Conversion System
