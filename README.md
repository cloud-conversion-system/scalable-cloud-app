# Scalable Cloud

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

### Despliegue del sistema de Cloud Storage

Para el despliegue del sistema de archivos de red, se ha actualizado la solución para utilizar Cloud Storage en lugar de NFS.

Para comenzar, se creó un bucket en Cloud Storage y se otorgaron los permisos necesarios para que la instancia pueda acceder a él. En las VM del worker y de la aplicación, se configuraron un par de parámetros adicionales para realizar la conexión con el bucket de Cloud Storage.

### Crea una plantilla de instancias para la ejecución de la aplicación.

- Selecciona máquinas de tipo N1 f1-micro.
- Disco de arranque Container-Optimized OS.
- Etiqueta de red http-server para permitir conexiones por el puerto 80.
- Añada una imagen de contenedor a la plantilla con la siguiente información:
    - En la imagen del contenedor coloque: `ghcr.io/cloud-conversion-system/scalable-cloud-app:main`
    - Agregue un volumen de tipo Directorio, en la ruta de activación ponga ```/app/credentials/``` como Ruta de activación y ```/var/credentials/``` como Ruta de acceso del host en Modo Lectura.
- Añade lo siguiente a automatización en "secuencia de comandos de inicio":

    ```
    #!bin/bash
    sudo mkdir /var/credentials/
    sudo rm /var/credentials/google-credentials.json
    sudo touch /var/credentials/google-credentials.json
    echo '<GOOGLE_CREDENTIALS>' | sudo tee -a /var/credentials/google-credentials.json
    ```

- Habilitar monitoring y logging

## Despliegue con Docker del worker
Puede utilizar Docker para inicializar la aplicación en GCP siguiendo las siguientes instrucciones:

En primer lugar, cree 1 instancia de VM utilizando Compute Engine y en una de ellas ejecute el worker. La ejecución de cada componente la podrá realizar de la siguiente forma:

```
sudo snap install docker
sudo docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/public-cloud-worker:main
sudo docker run --platform linux/amd64 ghcr.io/cloud-conversion-system/public-cloud-worker:main
```

## Documentación del API

[Postman Documentation](https://documenter.getpostman.com/view/11708390/2s93Y5NeWB)

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](LICENSE)**
- Copyright 2023 © Cloud Conversion System
