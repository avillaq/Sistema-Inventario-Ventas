# Sistema de Inventario y Ventas

## Descripción del Proyecto

El proyecto **Sistema de Inventario y Ventas** es una aplicación web desarrollada con Django y Python.  
El sistema permite gestionar productos, categorías, inventario y ventas mediante una interfaz web.

Entre sus funcionalidades principales se encuentran:

- Gestión de productos
- Control de inventario
- Registro de ventas
- Validación de stock
- Pruebas automáticas del sistema

Este documento tiene como finalidad explicar el proceso de instalación y ejecución del sistema para que otros usuarios puedan probar el proyecto correctamente.

---

# Requisitos del Sistema

Antes de ejecutar el proyecto, verificar que el equipo tenga instalado:

- Python 3.10 o superior
- Pip
- Navegador web (Google Chrome, Edge o Firefox)

---

# Instalación del Proyecto

## 1. Instalar Dependencias

Ejecutar el siguiente comando para instalar las librerías necesarias:

```bash
python -m pip install -r requirements.txt
```

---

## 2. Instalar pytest-django

Instalar `pytest-django` para ejecutar correctamente las pruebas automáticas:

```bash
pip install pytest-django
```

---

## 3. Aplicar Migraciones

Crear las tablas necesarias en la base de datos:

```bash
python manage.py migrate
```

---

## 4. Cargar Datos de Prueba

Cargar datos de demostración en el sistema:

```bash
python manage.py seed_demo
```

---

## 5. Ejecutar las Pruebas

Ejecutar las pruebas automáticas del proyecto:

```bash
python -m pytest -v
```

Si todo se ejecuta correctamente deberá mostrarse algo similar a:

```text
22 passed
```

---

## 6. Ejecutar el Servidor

Iniciar el servidor local del sistema:

```bash
python manage.py runserver
```

---

# Acceso al Sistema

Abrir el navegador web e ingresar al siguiente enlace:

http://127.0.0.1:8000

---

# Datos validos

- Producto: `stock` y `min_stock` entre 0 y 10,000.
- Producto: `price` mayor que 0; `cost` mayor o igual a 0.
- Cliente: `document_id` con 8 digitos y `phone` con 9 digitos.
- POS: cantidad de venta minimo 1 y maximo igual al stock disponible.

---

# Restricciones

- `barcode` de producto es unico.
- `document_id` y `email` de cliente son unicos si se registran.
- No se puede procesar venta sin cliente activo seleccionado.
- No se permite vender cantidad mayor al stock ni valores negativos.

---

# Recomendaciones para las Pruebas

Durante la evaluación del sistema se recomienda probar:

- Registro de productos
- Actualización de inventario
- Registro de ventas
- Validación de formularios
- Ingreso de datos inválidos
- Manejo de errores del sistema

---

# Observaciones

Seguir correctamente los pasos descritos en este manual permitirá ejecutar el sistema adecuadamente para realizar pruebas funcionales y detectar posibles errores del proyecto.
