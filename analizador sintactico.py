import sys
import re

class AnalizadorSintactico:
    def __init__(self):
        self.cadena = ""
        self.indice = 0

    # -------------------------
    # FUNCIÓN PRINCIPAL
    # -------------------------
    def main(self):
        print("Analizador sintáctico descendente:")
        nombre_archivo = input("Ingrese el nombre del archivo fuente: ")

        try:
            with open(nombre_archivo, 'r') as archivo:
                self.cadena = archivo.read()
        except IOError:
            print(f"Error al abrir el archivo: {nombre_archivo}")
            sys.exit(1)

        print("\n" + self.cadena + "\n")

        self.programa()

        if self.indice == len(self.cadena):
            print("Programa sintácticamente correcto")
        else:
            print("Error: programa incompleto o incorrecto")

    # -------------------------
    # PROGRAMA
    # -------------------------
    def programa(self):
        self.saltar_espacios()
        self.coincidir("begin")
        self.declaraciones()
        self.ordenes()
        self.coincidir("end")

    # -------------------------
    # DECLARACIONES
    # -------------------------
    def declaraciones(self):
        self.saltar_espacios()
        if (self.cadena.startswith("entero", self.indice) or 
            self.cadena.startswith("real", self.indice)):
            self.declaracion()
            self.resto_declaraciones()

    def resto_declaraciones(self):
        self.saltar_espacios()
        if self.indice < len(self.cadena) and self.cadena[self.indice] == ';':
            self.coincidir(";")
            self.declaraciones()

    def declaracion(self):
        self.tipo()
        self.lista_variables()

    def tipo(self):
        self.saltar_espacios()
        if self.cadena.startswith("entero", self.indice):
            self.coincidir("entero")
        elif self.cadena.startswith("real", self.indice):
            self.coincidir("real")
        else:
            self.mostrar_error("entero o real")

    def lista_variables(self):
        self.identificador()
        self.resto_lista_variables()

    def resto_lista_variables(self):
        self.saltar_espacios()
        if self.indice < len(self.cadena) and self.cadena[self.indice] == ',':
            self.coincidir(",")
            self.identificador()
            self.resto_lista_variables()

    # -------------------------
    # IDENTIFICADORES
    # -------------------------
    def identificador(self):
        self.letra()
        self.resto_letras()

    def letra(self):
        self.saltar_espacios()
        if self.indice < len(self.cadena) and self.cadena[self.indice].isalpha():
            self.coincidir(self.cadena[self.indice])
        else:
            self.mostrar_error("una letra")

    def resto_letras(self):
        while self.indice < len(self.cadena) and self.cadena[self.indice].isalnum():
            self.letraN()

    def letraN(self):
        if self.indice < len(self.cadena) and self.cadena[self.indice].isalnum():
            self.coincidir(self.cadena[self.indice])
        else:
            self.mostrar_error("una letra o un dígito")

    # -------------------------
    # ÓRDENES
    # -------------------------
    def ordenes(self):
        self.saltar_espacios()
        if (
            self.indice + 3 <= len(self.cadena) and self.cadena.startswith("end", self.indice)
            or self.indice + 7 <= len(self.cadena) and self.cadena.startswith("endwhile", self.indice)
            or self.indice == len(self.cadena)
        ):
            return
        
        self.orden()
        self.resto_ordenes()

    def resto_ordenes(self):
        self.saltar_espacios()
        if self.indice < len(self.cadena) and self.cadena[self.indice] == ';':
            self.coincidir(";")
            self.ordenes()

    def orden(self):
        self.saltar_espacios()
        if self.cadena.startswith("if", self.indice):
            self.condicion()
        elif self.cadena.startswith("end", self.indice) or self.cadena.startswith("endwhile", self.indice):
            self.coincidir("end")
        else:
            self.asignar()

    # -------------------------
    # CONDICIONES
    # -------------------------
    def condicion(self):
        self.coincidir("if")
        self.coincidir("(")
        self.comparacion()
        self.coincidir(")")
        self.coincidir("then")
        self.ordenes()
        self.resto_condicion()

    def resto_condicion(self):
        self.saltar_espacios()
        if self.cadena.startswith("end", self.indice):
            self.coincidir("end")
        elif self.cadena.startswith("else", self.indice):
            self.coincidir("else")
            self.ordenes()
            self.coincidir("end")

    def comparacion(self):
        self.expresion_arit()
        self.condicion_op()
        self.expresion_arit()

    def condicion_op(self):
        self.saltar_espacios()

        # Operadores de dos caracteres
        if self.cadena.startswith("<=", self.indice) or self.cadena.startswith(">=", self.indice) or self.cadena.startswith("<>", self.indice):
            self.indice += 2
            return

        # Operadores de un carácter
        if self.indice < len(self.cadena) and self.cadena[self.indice] in "=<>":
            self.coincidir(self.cadena[self.indice])
        else:
            self.mostrar_error("un operador de condición")

    # -------------------------
    # EXPRESIONES ARITMÉTICAS
    # -------------------------
    def expresion_arit(self):
        self.termino()
        self.expresion_arit_prime()

    def expresion_arit_prime(self):
        self.saltar_espacios()
        if self.indice < len(self.cadena) and self.cadena[self.indice] in '+-*/':
            self.operador_arit()
            self.termino()
            self.expresion_arit_prime()

    def termino(self):
        self.saltar_espacios()
        if self.indice < len(self.cadena) and self.cadena[self.indice] == '(':
            self.coincidir("(")
            self.expresion_arit()
            self.coincidir(")")
        elif self.indice < len(self.cadena) and self.cadena[self.indice].isalpha():
            self.identificador()
        elif self.indice < len(self.cadena) and self.cadena[self.indice].isdigit():
            self.numeros()
        else:
            self.mostrar_error("un término")

    def operador_arit(self):
        self.saltar_espacios()
        if self.indice < len(self.cadena) and self.cadena[self.indice] in '+-*/':
            self.coincidir(self.cadena[self.indice])
        else:
            self.mostrar_error("un operador aritmético")

    # -------------------------
    # ASIGNACIÓN
    # -------------------------
    def asignar(self):
        self.identificador()
        self.saltar_espacios()
        self.coincidir(":=")
        self.expresion_arit()

    # -------------------------
    # NÚMEROS
    # -------------------------
    def numeros(self):
        if self.indice < len(self.cadena) and self.cadena[self.indice].isdigit():
            self.numero_entero()
            if self.indice < len(self.cadena) and self.cadena[self.indice] == '.':
                self.coincidir(".")
                self.numero_entero()
        else:
            self.mostrar_error("un número")

    def numero_entero(self):
        if self.indice < len(self.cadena) and self.cadena[self.indice].isdigit():
            self.coincidir(self.cadena[self.indice])
            self.resto_entero()

    def resto_entero(self):
        while self.indice < len(self.cadena) and self.cadena[self.indice].isdigit():
            self.coincidir(self.cadena[self.indice])

    # -------------------------
    # UTILIDADES
    # -------------------------
    def coincidir(self, esperado):
        self.saltar_espacios()
        longitud = len(esperado)

        if self.cadena[self.indice:self.indice+longitud] == esperado:
            self.indice += longitud
            self.saltar_espacios()
        else:
            self.mostrar_error(esperado)

    def saltar_espacios(self):
        while self.indice < len(self.cadena) and self.cadena[self.indice].isspace():
            self.indice += 1

    def mostrar_error(self, esperado):
        fragmento = self.cadena[self.indice:self.indice+10]
        print(f"Error: se esperaba '{esperado}', pero se encontró '{fragmento}'")
        sys.exit(1)


# -------------------------
# EJECUTAR ANALIZADOR
# -------------------------
if __name__ == "__main__":
    analizador = AnalizadorSintactico()
    analizador.main()
