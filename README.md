# Aliens API REST
API para resolver el problema de interpretación del lenguaje alienígena, utilizando el framework Flask.




## Pre-requisitos 📋

* Se necesita [python3](https://www.python.org/download/releases/3.0/).
* Gestor de paquetes [pip](https://pip.pypa.io/en/stable/).
* El módulo para gestionar ambientes virtuales [python3-venv](https://pypi.org/project/virtualenv/).

### Ejecucion larga🔧

* Descargar o clonar el repositorio.
* En un terminal dirigirse a la carpeta en que se realizó la descarga y ejecutar lo siguiente.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -U setuptools
pip install -r requirements.txt
export DATABASE=connection_string
uwsgi config.ini
```
Ejecutando lo anterior el servicio estará corriendo en [http://localhost:8000/](http://localhost:8000/)

### Ejecucion con Docker🔧



* Descargar o clonar el repositorio.
* En un terminal dirigirse a la carpeta en que se realizó la descarga y ejecutar lo siguiente.
```sh
docker build -t flask-alien:latest .
docker run -d -e DATABASE=connection_string -p 8080:8000 flask-alien
```
Ejecutando lo anterior el contenedor estará corriendo en [http://localhost:8080/](http://localhost:8080/)

## Autor ✒️

* **Oscar Cerda**