# Public Cloud

REST Backend + Asynchronous Processing Layer. Basic deployment in the public cloud.

This application allows compressing files using different utilities and/or algorithms: ZIP, 7Z, TAR.GZ, TAR.BZ2

## Video Explicativo

[YouTube Link](https://youtu.be/bWWDLfnUB4c)

## Documentación del API

[Postman Documentation](https://documenter.getpostman.com/view/11708390/2s93Y5NeWB)

## ¿Cómo desplegar la aplicación en GCP?

### Despliegue de la base de datos

En primer lugar cree una instancia de Cloud SQL en la misma región en la que creó las instancias de Compute Engine. Asegurese que utilice PostgreSQL 14.

Luego, chequee la opción de asignar IP privada, esta es la que va a utilizar para hacer llamado en la base de datos.
Verifique que la maquina pertenezca a la misma VPC que las demás maquinas desplegadas.

Luego de haber chequeado la opción, en caso de que su proyecto no tenga activadas las APIs necesarias, GCP lo redirigirá a un tutorial para activarlas y asignar correctamente esa IP privada a la VPC correspondiente.

Una vez la instancia se haya creado, reemplace la IP de la base de datos contenida en los archivos ```celery_script/tasks``` y ```__init__.py```. Solo debe reemplazar la parte contenida después del @ y antes del /.

### Despliegue del sistema de archivos de red (NFS)

Para empezar, cree una instancia de VM utilizando Compute Engine, asegurándome que sigan las mismas especificaciones que las máquinas virtuales que representan el worker y la aplicacion.

Seguidamente, en esta instancia instalé el nfs-kernel-server que permite establecer la carpeta compartida y todas las configuraciones de esta. Para ello, cree un directorio (el que se va a compartir) y modifiqué el archivo /etc/exports/ en el cual se especifica el directorio compartido, que maquinas van a poder acceder (ips), los permisos (rw), entre otras. Por último, reinicié el este servicio.

En las VM del worker y de la app se configuraron un par de parámetros extra para realizar esta conexión. A la hora de hacer el docker.run, se debió agregar el condigo adicional “-v /mnt/nfs/cloud-conversion-tool/files:/python-docker/cloud_conversion_tool/files” que vincula la carpeta existente dentro de la instancia NFS y una carpeta de interés dentro de las instancias worker y app. De esta manera, lo que se suba en esta carpeta va ser visible y se van a poder descargar los contenidos en las demás.

### Despliegue con Docker

Puede utilizar Docker para inicializar la aplicación en GCP siguiendo las siguientes instrucciones:

En primer lugar, cree 2 instancias de VM utilizando Compute Engine y en una de ellas ejecute el worker y en la otra la aplicación. La ejecución de cada componente la podrá realizar de la siguiente forma:

#### Vincular NFS con el worker y la aplicación

En la instancia del worker y la aplicación deberá vincular el sistema de archivos de red para la escritura en el directorio compartido.

```bash
sudo mount <internal-file-server-ip>:/user-files /mnt/nfs
```

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
