SECTION .data  
    msg db 'Hola mundo!', 0Ah
SECTION .text
global _start
_start:

    ;--------- calculo de longitud de cadena --------
    strlen:
        push ebx
        mov ebx, eax
    nextChar:
        cmp byte [eax], 0
        jz finLen
        inc eax
        jpm nextChar

    finLen:
    sub aex, ebx
    pop ebx
    ret

    ;----------- imprimir printstr(msg) ----------------
    ; guardar registros en pila
    push edx
    push ecx
    push ebx
    push eax ; aca apunta a la cadena

    ;------- calcular longitud de cadena -----------
    call strlen
    mov edx, eax ;longitud de cadena
    pop eax
    mov ecx, eax
    mov ecx, eax ;cadena a imprimir
    mov ebx, 1 ;tipo de salida (STDOUT file)
    mov eax, 4 ;SYS_WRITE (kernel opocode 4)
    int 80h

    pop ebx
    pop ecx
    pop edx
    ret

_end:
    ;-----------end----------------
    mov ebx, 0 ;return 0 status on exit
    mov eax, 1 ;SYS_EXIT (kernel opocode 1)
    int 80h