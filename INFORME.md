# Informe

Sistema de Inventario y Ventas

## Integrantes

- Juan Sergio Zeballos Perez
- Chambi Velasquez, Rommel Abraham
- Villafuerte Quispe Alexander
- Huarca Pallani Jael Emerson

## Descripcion

El proyecto **Sistema de Inventario y Ventas** es una aplicacion web desarrollada con Django y Python.
Permite gestionar productos, inventario, clientes y ventas mediante una interfaz web.

## Validaciones

- Producto: `stock` y `min_stock` entre 0 y 10,000.
- Producto: `price` mayor que 0; `cost` mayor o igual a 0.
- Cliente: `document_id` con 8 digitos y `phone` con 9 digitos.
- POS: cantidad de venta minimo 1 y maximo igual al stock disponible.
- Venta: requiere cliente activo seleccionado para procesar cobro.

## Casos PE (implementados)

Los casos se validan con pruebas UI automatizadas. El codigo mostrado es real y proviene de los tests.

### Inventario

| Caso (PE) | Datos de prueba | Resultado esperado | Codigo de prueba |
| --- | --- | --- | --- |
| Stock no numerico | `stock="abc"` o `stock="@@@"` | El input conserva el valor numerico previo | `stock_input.type(invalid_value)`<br>`value = stock_input.input_value()`<br>`assert value == "0"` |
| Stock/min_stock rango numerico | `value in {-1, 0, 1, 9999, 10000, 10001}` | Fuera de rango invalido; dentro de rango valido | `[(-1, False), (0, True), (1, True), (9999, True), (10000, True), (10001, False)],`<br>`input_field.fill(str(value))`<br>`assert is_valid is expected_valid` |

### POS / Caja

| Caso (PE) | Datos de prueba | Resultado esperado | Codigo de prueba |
| --- | --- | --- | --- |
| Cantidad invalida | `0` | El item se elimina del carrito | `qty_input.fill("0")`<br>`qty_input.press("Tab")`<br>`expect(empty_state).to_be_visible()` |
| Cantidad mayor al stock | `stock + 1` (ej. 5 con stock 2) | Se ajusta al maximo y se deshabilita `+` | `qty_input.fill("5")`<br>`qty_input.press("Tab")`<br>`expect(qty_input).to_have_value(str(product.stock))`<br>`expect(plus_button).to_be_disabled()` |
| Cantidad valida | `1` | Se mantiene en el carrito | `expect(qty_input).to_have_value("1")` |

### Clientes

| Caso (PE) | Datos de prueba | Resultado esperado | Codigo de prueba |
| --- | --- | --- | --- |
| Documento: longitud invalida/valida | `1234567` (invalido), `12345678` (valido) | Validacion del input segun longitud | `[("1234567", False), ("12345678", True)],`<br>`input_field.fill(document_id)`<br>`assert is_valid is expected_valid` |
| Documento: longitud maxima | `123456789` | El input recorta a 8 digitos | `input_field.type("123456789")`<br>`value = input_field.input_value()`<br>`assert value == "12345678"` |
| Telefono: longitud invalida/valida | `12345678` (invalido), `123456789` (valido) | Validacion del input segun longitud | `[("12345678", False), ("123456789", True)],`<br>`input_field.fill(phone)`<br>`assert is_valid is expected_valid` |
| Telefono: longitud maxima | `1234567890` | El input recorta a 9 digitos | `input_field.type("1234567890")`<br>`value = input_field.input_value()`<br>`assert value == "123456789"` |

## Casos AVL (implementados)

### Inventario

| Caso (AVL) | Datos de prueba | Resultado esperado | Codigo de prueba |
| --- | --- | --- | --- |
| Limites inferior y superior de `stock` y `min_stock` | `-1, 0, 1, 9999, 10000, 10001` | `-1` y `10001` invalidos; resto validos | `[(-1, False), (0, True), (1, True), (9999, True), (10000, True), (10001, False)],`<br>`input_field.fill(str(value))`<br>`assert is_valid is expected_valid` |

### POS / Caja

| Caso (AVL) | Datos de prueba | Resultado esperado | Codigo de prueba |
| --- | --- | --- | --- |
| Limite minimo | `0` | El item se elimina del carrito | `qty_input.fill("0")`<br>`qty_input.press("Tab")`<br>`expect(empty_state).to_be_visible()` |
| Limite maximo | `stock + 1` (ej. 5 con stock 2) | Se ajusta al stock y se deshabilita `+` | `qty_input.fill("5")`<br>`qty_input.press("Tab")`<br>`expect(qty_input).to_have_value(str(product.stock))`<br>`expect(plus_button).to_be_disabled()` |

### Clientes

| Caso (AVL) | Datos de prueba | Resultado esperado | Codigo de prueba |
| --- | --- | --- | --- |
| Documento: limite inferior | `1234567` (invalido), `12345678` (valido) | Validacion del input segun longitud | `[("1234567", False), ("12345678", True)],`<br>`input_field.fill(document_id)`<br>`assert is_valid is expected_valid` |
| Documento: limite superior | `123456789` | El input recorta a 8 digitos | `input_field.type("123456789")`<br>`value = input_field.input_value()`<br>`assert value == "12345678"` |
| Telefono: limite inferior | `12345678` (invalido), `123456789` (valido) | Validacion del input segun longitud | `[("12345678", False), ("123456789", True)],`<br>`input_field.fill(phone)`<br>`assert is_valid is expected_valid` |
| Telefono: limite superior | `1234567890` | El input recorta a 9 digitos | `input_field.type("1234567890")`<br>`value = input_field.input_value()`<br>`assert value == "123456789"` |

## Notas

- Ventas e historial y Dashboard no tienen casos PE/AVL implementados ni pruebas UI asociadas.
