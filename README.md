# Public Cloud

REST Backend + Asynchronous Processing Layer. Basic Deployment in the Public Cloud.

This application allows compressing files using different utilities and/or algorithms: ZIP, 7Z, TAR.GZ, TAR.BZ2

## Video Explicativo

TODO: [YouTube Link]()

## Documentación del API

[Postman Documentation](https://documenter.getpostman.com/view/11708390/2s93Y5NeWB)

## ¿Cómo desplegar la aplicación en GCP?

### Despliegue de la base de datos

En primer lugar cree una instancia de Cloud SQL en la misma región en la que creó las instancias de Compute Engine. Asegurese que utilice PostgreSQL 14.  

Luego, chequee la opción de asignar IP privada, esta es la que va a utilizar para hacer llamado en la base de datos.  
Verifique que la maquina pertenezca a la misma VPC que las demás maquinas desplegadas.

Luego de haber chequeado la opción, en caso de que su proyecto no tenga activadas las APIs necesarias, GCP lo redirigirá a un tutorial para activarlas y asignar correctamente esa IP privada a la VPC correspondiente.  

Una vez la instancia se haya creado, reemplace la IP de la base de datos contenida en los archivos ```celery_script/tasks``` y ```__init__.py```. Solo debe reemplazar la parte contenida después del @ y antes del /.

### Despliegue con Docker

Puede utilizar Docker para inicializar la aplicación en GCP siguiendo las siguientes instrucciones:

En primer lugar, cree 2 instancias de VM utilizando Compute Engine y en una de ellas ejecute el worker y en la otra la aplicación. La ejecución de cada componente la podrá realizar de la siguiente forma:

#### Ejecución del worker

```bash
sudo snap install docker
sudo docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/public-cloud-worker:main
sudo docker run --platform linux/amd64 -v /mnt/nfs/cloud-conversion-tool/files:/python-docker/cloud_conversion_tool/files ghcr.io/cloud-conversion-system/public-cloud-worker:main
```

#### Ejecución de la aplicación:

```bash
sudo snap install docker
sudo docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/public-cloud-app:main
sudo docker run --platform linux/amd64 -p 80:80 -v /mnt/nfs/cloud-conversion-tool/files:/python-docker/cloud_conversion_tool/files ghcr.io/cloud-conversion-system/public-cloud-app:main
```

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](LICENSE)**
- Copyright 2023 © Cloud Conversion System
