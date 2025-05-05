section .data
    ; Formatos para printf/scanf
    fmt_int    db "%d", 0        ; Formato para enteros
    fmt_float  db "%f", 0        ; Formato para flotantes
    fmt_string db "%s", 0        ; Formato para strings

section .text
    ; Importar funciones de msvcrt.dll (biblioteca estándar de C en Windows)
    extern _printf, _scanf, _exit

; -------------------- printf --------------------
; Argumentos:
;   rcx: formato (ej: "Valor: %d")
;   rdx, r8, r9, pila: valores a imprimir
_printf_win:
    sub rsp, 32             ; Shadow space (32 bytes para llamadas a WinAPI)
    call _printf
    add rsp, 32
    ret

; -------------------- scanf --------------------
; Argumentos:
;   rcx: formato (ej: "%d")
;   rdx: dirección de la variable donde guardar el valor
_scanf_win:
    sub rsp, 32             ; Shadow space
    call _scanf
    add rsp, 32
    ret

; -------------------- exit --------------------
_exit_win:
    mov rcx, 0              ; Código de salida
    call _exit