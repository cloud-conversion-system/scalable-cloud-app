# Public Cloud

REST Backend + Asynchronous Processing Layer. Basic Deployment in the Public Cloud.

This application allows compressing files using different utilities and/or algorithms: ZIP, 7Z, TAR.GZ, TAR.BZ2

## Video Explicativo

TODO: [YouTube Link]()

## ¿Cómo desplegar la aplicación en GCP?

### Despliegue con Docker

Puede utilizar Docker para inicializar la aplicación en GCP siguiendo las siguientes instrucciones:

En primer lugar, cree 2 instancias de VM utilizando Compute Engine y en una de ellas ejecute el worker y en la otra la aplicación. La ejecución de cada componente la podrá realizar de la siguiente forma:

#### Ejecución del worker

```bash
sudo snap install docker
sudo docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/public-cloud-worker:main
sudo docker run --platform linux/amd64 -i ghcr.io/cloud-conversion-system/public-cloud-worker:main
```

#### Ejecución de la aplicación:

```bash
sudo snap install docker
sudo docker pull --platform linux/x86_64 ghcr.io/cloud-conversion-system/public-cloud-app:main
sudo docker run --platform linux/amd64 -p 80:80 -i ghcr.io/cloud-conversion-system/public-cloud-app:main
```

## License

[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

- **[MIT license](LICENSE)**
- Copyright 2023 © Cloud Conversion System
