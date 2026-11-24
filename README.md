# Gestor de productos
 
Programa de consola en Python para listar, agregar, quitar y buscar productos.
Los datos se guardan en una base de datos SQLite (`productos.db`), por lo que
se conservan al cerrar el programa y se recuperan al volver a abrirlo.
 
## Requisitos
 
- Python 3.10 o superior (probado con Python 3.14)
- La librería `rich` (se usa para mostrar las tablas y los colores)
## Instalación y ejecución
 
Desde una terminal, dentro de la carpeta del proyecto:
 
```
pip install -r requirements.txt
python main.py
```
 
La base de datos `productos.db` se crea sola la primera vez que se ejecuta el
programa. No hace falta instalar nada más para usar SQLite: viene incluido con
Python.
 
## Uso con entorno virtual
 
Si se prefiere no instalar `rich` en el Python general de la computadora, se
puede crear un entorno virtual antes de instalar. Los pasos cambian según el
sistema.
 
Windows (PowerShell):
 
```
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```
 
Si PowerShell bloquea la activación, ejecutar primero:
`Set-ExecutionPolicy -Scope Process RemoteSigned`
 
Windows (cmd):
 
```
python -m venv .venv
.venv\Scripts\activate.bat
pip install -r requirements.txt
python main.py
```
 
Mac o Linux:
 
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```
 
Con el entorno activado, la línea de la terminal empieza con `(.venv)`.