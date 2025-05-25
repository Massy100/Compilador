
    section .data
        ; Variables enteras (32 bits)
        x          dd 0       ; Define 'x' como entero de 32 bits
        valor      dd 0       ; Define 'valor'
        i          dd 0       ; Define 'i'
        resultado  dd 0       ; Define 'resultado'
        
        ; Constantes flotantes (32 bits)
        pi         dd 3.14159 ; Define 'pi' como float (32 bits)
        diametro   dd 8.0     ; Define 'diametro' como float
        
        ; Variables flotantes (32 bits)
        circunferencia dd 0.0 ; Variable para el resultado flotante

    section .bss
        ; Este espacio es para inicializar variables en caso de necesidad

    section .text
        global _condicional   ; Hace visible la funcion 'condicional'
        global _calcular_circunferencia ; Funcion flotante
        global _main          ; Hace visible la funcion 'main' (con _ para MinGW)

    #include <stdio.h>

void hola() {
    printf("Hola");
}

int main() {
    hola();
}

