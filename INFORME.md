# Informe

Sistema de Inventario y Ventas

## Integrantes

- Juan Sergio Zeballos Perez
- Chambi Velasquez, Rommel Abraham
- Villafuerte Quispe Alexander
- Huarca Pallani Jael Emerson

## Descripcion

El proyecto **Sistema de Inventario y Ventas** es una aplicación web desarrollada con Django y Python.  
El sistema permite gestionar productos, categorías, inventario y ventas mediante una interfaz web.

Entre sus funcionalidades principales se encuentran:

- Gestión de productos
- Control de inventario
- Registro de ventas
- Validación de stock
- Pruebas automáticas del sistema

## Validaciones

- Producto: `stock` y `min_stock` entre 0 y 10,000.
- Producto: `price` mayor que 0; `cost` mayor o igual a 0.
- Cliente: `document_id` con 8 digitos y `phone` con 9 digitos.
- POS: cantidad de venta minimo 1 y maximo igual al stock disponible.

## Casos PE

- Inventario (stock): negativos y mayores a 10,000 rechazados; valores dentro del rango aceptados.
- Inventario UI: letras o simbolos en `stock` no son aceptados por el navegador.
- POS: cantidad cero/negativa o mayor al stock rechazada; cantidad valida aceptada.

## Casos AVL

- Inventario (stock): -1 rechazado, 0 aceptado, 1 aceptado; 9,999 aceptado, 10,000 aceptado, 10,001 rechazado.
- POS (cantidad): 0 rechazado, 1 aceptado; `stock` aceptado, `stock + 1` rechazado.
