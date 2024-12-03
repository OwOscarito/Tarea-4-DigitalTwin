# Proyecto 1 

## Descripcion
Representacion dgital de la orientacion de un sensor BMI270

## Instrucciones de uso

### Codigo esp:
1. Compilar y flashear a la esp32
```py
idf.py build flash
```
### App python:
Entrar a la carpeta digital twin

1. Crear venv y cargarlo
```sh
python -m venv venv
```
En linux:
```sh
source venv/bin/activate
```
En windows:
```ps1
venv/Scripts/activate
```
2. Instalar requirements.txt
```sh
pip install -r requirements.txt
```
3. Comprobar el puerto de comunicacion serial en el archivo receiver.py
```py
PORT = "___" # Reemplazar por el puerto correspondiente
```
4. Ejecutar main.py
```sh
python main.py
```