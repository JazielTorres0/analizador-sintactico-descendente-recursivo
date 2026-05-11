# Analizador Sintáctico Descendente Recursivo

## Descripción

Este proyecto implementa un **analizador sintáctico descendente recursivo** desarrollado en Python.  
El programa lee un archivo fuente escrito en un lenguaje simple definido por una gramática específica y verifica si su estructura sintáctica es correcta.

El analizador reconoce:

- Declaraciones de variables
- Tipos de datos (`entero`, `real`)
- Asignaciones
- Expresiones aritméticas
- Condiciones `if`
- Bloques `begin` y `end`

Si el programa cumple la gramática establecida, el sistema muestra:

```txt
Programa sintácticamente correcto
```

En caso contrario, se reporta un error indicando qué símbolo se esperaba.

---

# Características

- Analizador sintáctico descendente recursivo
- Manejo de identificadores y números
- Soporte para expresiones aritméticas
- Validación de estructuras condicionales
- Detección de errores sintácticos
- Implementado completamente en Python

---

# Tecnologías utilizadas

- Python 3

Librerías utilizadas:

```python
sys
re
```

---

# Estructura general del lenguaje

El lenguaje soporta estructuras como:

```txt
begin
entero x, y;
real z;

x := 10;
y := 20;

if (x < y) then
    z := x + y
end

end
```

---

# Gramática simplificada

## Programa

```txt
programa → begin declaraciones ordenes end
```

## Declaraciones

```txt
declaraciones → declaracion resto_declaraciones
```

## Declaración

```txt
declaracion → tipo lista_variables
```

## Tipos

```txt
tipo → entero | real
```

## Asignación

```txt
asignar → identificador := expresion_arit
```

## Condición

```txt
condicion → if (comparacion) then ordenes end
```

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/repositorio.git
```

## 2. Entrar a la carpeta

```bash
cd repositorio
```

## 3. Ejecutar el programa

```bash
python analizador.py
```

---

# Uso

El programa solicitará el nombre del archivo fuente:

```txt
Ingrese el nombre del archivo fuente:
```

Ejemplo:

```txt
programa.txt
```

---

# Ejemplo de entrada

Archivo:

```txt
begin
entero a, b;
real c;

a := 5;
b := 10;

if (a < b) then
    c := a + b
end

end
```

---

# Ejemplo de salida correcta

```txt
Programa sintácticamente correcto
```

---

# Ejemplo de error

Entrada incorrecta:

```txt
begin
entero x
x := 5
end
```

Salida:

```txt
Error: se esperaba ';'
```

---

# Funcionamiento interno

El proyecto utiliza parsing descendente recursivo mediante funciones que representan reglas gramaticales.

Ejemplo:

```python
def expresion_arit(self):
    self.termino()
    self.expresion_arit_prime()
```

Cada método procesa una producción específica de la gramática.

---

# Limitaciones

Actualmente el analizador:

- No realiza análisis semántico
- No genera código máquina
- No posee tabla de símbolos
- No implementa análisis léxico separado
- No compila programas reales

El proyecto se enfoca únicamente en el análisis sintáctico.

---

# Posibles mejoras

- Implementar analizador léxico
- Crear tabla de símbolos
- Validación semántica
- Soporte para ciclos `while`
- Generación de código intermedio
- Generación de código ensamblador

