# Sistema de Inventario y Ventas

## Descripcion del proyecto

El proyecto **Sistema de Inventario y Ventas** es una aplicación web desarrollada con Django y Python.  
El sistema permite gestionar productos, inventario, clientes y ventas mediante una interfaz web.

### Funcionalidades principales

- Catalogo de productos con control de stock.
- POS con carrito en tiempo real y validaciones de cantidad.
- Historial de ventas con filtros.
- Gestion de clientes con validaciones basicas.

---

## Requisitos del sistema

- Python 3.10 o superior
- Pip
- Navegador web (Chrome, Edge o Firefox)

---

## Como ejecutar el programa

1. Instalar dependencias:
	```bash
	python -m pip install -r requirements.txt
	```
2. Aplicar migraciones:
	```bash
	python manage.py migrate
	```
3. Cargar datos de prueba:
	```bash
	python manage.py seed_demo
	```
4. Iniciar el servidor:
	```bash
	python manage.py runserver
	```
5. Abrir el sistema en el navegador:
	```text
	http://127.0.0.1:8000
	```

---

## Pruebas

- Ejecutar toda la suite:
  ```bash
  python -m pytest -q
  ```
- Ejecutar con salida detallada:
  ```bash
  python -m pytest -v
  ```

---

## Datos validos

- Producto: `stock` y `min_stock` entre 0 y 10,000.
- Producto: `price` mayor que 0; `cost` mayor o igual a 0.
- Cliente: `document_id` con 8 digitos y `phone` con 9 digitos.
- POS: cantidad de venta minimo 1 y maximo igual al stock disponible.

---

## Restricciones

- `barcode` de producto es unico.
- `document_id` y `email` de cliente son unicos si se registran.
- No se puede procesar venta sin cliente activo seleccionado.
- No se permite vender cantidad mayor al stock ni valores negativos.

---

## Recomendaciones para pruebas manuales

- Crear, editar y eliminar productos.
- Probar limites de stock y min_stock.
- Procesar ventas con cantidades validas e invalidas.
- Registrar clientes con DNI y telefono validos.

---

## Observaciones

Seguir estos pasos asegura la ejecucion correcta del sistema y permite validar los flujos principales con datos reales y pruebas automatizadas.
