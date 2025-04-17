section .data
    x          dd 0     ; Define 'x' como entero de 32 bits
    valor      dd 0     ; Define 'valor'
    i          dd 0     ; Define 'i'
    resultado  dd 0     ; Define 'resultado'

section .text
    global _condicional  ; Hace visible la función 'condicional'
    global _main        ; Hace visible la función 'main' (con _ para MinGW)

_condicional:
    push ebp
    mov ebp, esp
    mov eax, [x] ; cargar variable x
    push eax
    mov eax, 0 ; cargar constante 0
    pop ebx
    cmp ebx, eax
    setg al
    movzx eax, al
    cmp eax, 0
    je L2208800188240_next
    mov eax, 1 ; cargar constante 1
    ret ; retorno desde la subrutina
    jmp L2208800188240_end
L2208800188240_next:
    mov eax, [x] ; cargar variable x
    push eax
    mov eax, 0 ; cargar constante 0
    pop ebx
    cmp ebx, eax
    setl al
    movzx eax, al
    cmp eax, 0
    je L2208800188240_next_0
    mov eax, -1 ; cargar constante -1
    ret ; retorno desde la subrutina
    jmp L2208800188240_end
L2208800188240_next_0:
    mov eax, 0 ; cargar constante 0
    ret ; retorno desde la subrutina
L2208800188240_end:
    mov esp, ebp
    pop ebp
    ret


_main:
    push ebp
    mov ebp, esp
    mov eax, 5 ; cargar constante 5
    mov [valor], eax ; asignar a valor
L2208800188960_start: ; inicio de bucle while
    mov eax, [valor] ; cargar variable valor
    push eax
    mov eax, 0 ; cargar constante 0
    pop ebx
    cmp ebx, eax
    setg al
    movzx eax, al
    cmp eax, 0 ; comparar la condicion de bucle while
    je L2208800188960_end ; terninar el bucle si la condicion es falsa
    mov eax, [valor] ; cargar variable valor
    push eax; guardar en la pila
    mov eax, 1 ; cargar constante 1
    pop ebx; recuperar el primer operando
    sub ebx, eax; ebx = ebx - eax
    mov eax, ebx; eax = ebx
    mov [valor], eax ; asignar a valor
    jmp L2208800188960_start ; volvar al inicio del bucle while
L2208800188960_end: ; fin de bucle while
    mov eax, 0 ; cargar constante 0
    mov [i], eax ; asignar a i
L2208800189584_start: ; inicio del bucle for
    mov eax, [i] ; cargar variable i
    push eax
    mov eax, 1 ; cargar constante 1
    pop ebx
    cmp ebx, eax
    setle al
    movzx eax, al
    cmp eax, 0 ; comparar la condicion del for
    je L2208800189584_end ; salir del bucle si la condicion es falsa
    mov eax, [valor] ; cargar variable valor
    push eax; guardar en la pila
    mov eax, 1 ; cargar constante 1
    pop ebx; recuperar el primer operando
    add eax, ebx ; eax = eax + ebx
    mov [valor], eax ; asignar a valor
    mov eax, [i]
    add eax, 1
    mov [i], eax  ; i++
    jmp L2208800189584_start ; volver al inicio del bucle for
L2208800189584_end: ; fin del bucle for
    mov eax, [valor] ; cargar variable valor
    push eax
    call _condicional
    add esp, 4
    mov [resultado], eax ; asignar a resultado
    mov esp, ebp
    pop ebp
    ret


