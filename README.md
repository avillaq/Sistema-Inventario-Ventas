# Sistema Inventario Ventas

Sistema web desarrollado con Django y Python para la gestión de inventario y ventas.

## Requisitos

- Python 3.10 o superior
- Pip

## Instalación

Ejecutar los siguientes comandos en orden:

```bash
python -m pip install -r requirements.txt
pip install pytest-django
python manage.py migrate
python manage.py seed_demo
python -m pytest -q
python manage.py runserver
```

## Acceso al sistema

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

## Resultado esperado de pruebas

```text
7 passed
```

## Manual completo

El manual completo se encuentra en el archivo PDF del repositorio.
