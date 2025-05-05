; Manejo de valores de coma flotante - Versión Windows x64

extern printf

SECTION .data
    pi:       dq   3.14159
    diametro: dq   5.0
    format:   db   "C = pi*d = %f * %f = %f", 10, 0

SECTION .bss
    c:       resq    1

SECTION .text
    global main

main:
    sub     rsp, 40         ; Reservar espacio en la pila (32 bytes shadow space + 8 para alineación)
    
    ; Cálculo del perímetro
    fld     qword [diametro]
    fmul    qword [pi]
    fstp    qword [c]
    
    ; Preparar parámetros para printf
    ; En Windows x64, los primeros 4 parámetros flotantes van en xmm0-xmm3
    movq    rdx, qword [c]      ; Cargar c en RDX para pasarlo a la pila
    movq    xmm2, rdx           ; Mover a xmm2 (tercer parámetro flotante)
    movq    xmm1, qword [diametro] ; Segundo parámetro flotante
    movq    xmm0, qword [pi]    ; Primer parámetro flotante
    
    ; En Windows, los parámetros adicionales se pasan en la pila
    mov     rcx, format         ; Primer parámetro (cadena de formato)
    mov     rax, 2              ; Número de registros vectoriales usados (xmm0-xmm2 = 3, pero parece que se usa 2)
    
    ; Asegurar alineación de pila a 16 bytes
    sub     rsp, 32             ; Shadow space para printf
    call    printf
    add     rsp, 32             ; Limpiar shadow space
    
    ; Retornar
    add     rsp, 40             ; Restaurar pila
    xor     eax, eax            ; Código de retorno 0
    ret