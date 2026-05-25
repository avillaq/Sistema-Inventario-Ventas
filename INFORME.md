# Informe

Sistema de Inventario y Ventas

## Integrantes

- Juan Sergio Zeballos Perez
- Chambi Velasquez, Rommel Abraham
- Villafuerte Quispe Alexander
- Huarca Pallani Jael Emerson

## Descripcion

El proyecto **Sistema de Inventario y Ventas** es una aplicación web desarrollada con Django y Python.  
El sistema permite gestionar productos, inventario, clientes y ventas mediante una interfaz web.

## Validaciones

- Producto: `stock` y `min_stock` entre 0 y 10,000.
- Producto: `price` mayor que 0; `cost` mayor o igual a 0.
- Cliente: `document_id` con 8 digitos y `phone` con 9 digitos.
- POS: cantidad de venta minimo 1 y maximo igual al stock disponible.
- Venta: requiere cliente activo seleccionado para procesar cobro.

## Casos PE (implementados)

### Inventario

- No numerico en `stock`: el navegador bloquea letras o simbolos.
- Fuera de rango: valores menores a 0 o mayores a 10,000 son invalidos.
- Dentro de rango: valores validos aceptados.

### POS / Caja

- Cantidad invalida: 0 elimina el item del carrito.
- Cantidad mayor al stock: se ajusta al maximo disponible y se deshabilita el boton `+`.
- Cantidad valida: se mantiene en el carrito.

### Clientes

- Documento: 7 digitos invalido, 8 digitos valido.
- Telefono: 8 digitos invalido, 9 digitos valido.
- Longitud maxima: los inputs recortan a 8 y 9 digitos respectivamente.

### Ventas e historial

- Sin PE aplicable: los filtros son libres y no tienen limites numericos definidos.

### Dashboard

- Sin PE aplicable: no existen entradas de datos en la pantalla.

## Casos AVL (implementados)

### Inventario

- `stock` y `min_stock`: -1 rechazado, 0 aceptado, 1 aceptado.
- Limite superior: 9,999 aceptado, 10,000 aceptado, 10,001 rechazado.

### POS / Caja

- Limite minimo: 0 elimina item, 1 acepta cantidad.
- Limite maximo: `stock` aceptado, `stock + 1` ajustado al maximo.

### Clientes

- Documento: 7 (invalido), 8 (valido), 9 recortado a 8.
- Telefono: 8 (invalido), 9 (valido), 10 recortado a 9.
