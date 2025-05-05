%include 'ensamblador.asm'
SECTION .data  
    msg db 'Hola mundo!', 0Ah, 0
SECTION .text
global _start

_start:
    ;------- Imprimir print(msg) -------
    mov eax, msg
    call printstr

    ;------- end -------------
    call quit