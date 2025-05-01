
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

    _condicional:
    push ebp
    mov ebp, esp
    mov eax, [x] ; cargar variable x
    push eax
    mov eax, 0 ; cargar entero 0
    pop ebx
    cmp ebx, eax
    setg al
    movzx eax, al
    cmp eax, 0
    je L1930269439376_next
    mov eax, 1 ; cargar entero 1
    ret ; retorno desde la subrutina
    jmp L1930269439376_end
L1930269439376_next:
    mov eax, [x] ; cargar variable x
    push eax
    mov eax, 0 ; cargar entero 0
    pop ebx
    cmp ebx, eax
    setl al
    movzx eax, al
    cmp eax, 0
    je L1930269439376_next_0
    mov eax, -1 ; cargar entero -1
    ret ; retorno desde la subrutina
    jmp L1930269439376_end
L1930269439376_next_0:
    mov eax, 0 ; cargar entero 0
    ret ; retorno desde la subrutina
L1930269439376_end:
    mov esp, ebp
    pop ebp
    ret


calcular_circunferencia
    push ebp
    mov ebp, esp
    pi dd 3.14159f ; constante float
    mov eax, [pi] ; cargar variable pi
    push eax; guardar en la pila
    mov eax, [diametro] ; cargar variable diametro
    pop ebx; recuperar el primer operando
    ret ; retorno desde la subrutina
    mov esp, ebp
    pop ebp
    ret


pedir:
    push ebp
    mov ebp, esp
; Declaracion de variable: int numero
    mov eax, "Por favor, ingresa un numero entero: " ; cargar string
    push eax
    call _printf
    add esp, 4
    mov eax, [numero] ; cargar variable numero
    push eax
    mov eax, "%d" ; cargar string
    push eax
    call _scanf
    add esp, 8
    mov eax, [numero] ; cargar variable numero
    push eax
    mov eax, "El numero que ingresaste es: %d\n" ; cargar string
    push eax
    call _printf
    add esp, 8
    mov esp, ebp
    pop ebp
    ret


_main:
    push ebp
    mov ebp, esp

    mov eax, 5 ; cargar entero 5
    mov [valor], eax ; asignar a valor
    mov eax, 8 ; cargar entero 8
    mov [diametro_entero], eax ; asignar a diametro_entero
    movss xmm0, [3.14159f] ; cargar flotante 3.14159f
    mov [pi], eax ; asignar a pi
    movss xmm0, [8.0f] ; cargar flotante 8.0f
    mov [diametro], eax ; asignar a diametro
L1930269441152_start: ; inicio de bucle while
    mov eax, [valor] ; cargar variable valor
    push eax
    mov eax, 0 ; cargar entero 0
    pop ebx
    cmp ebx, eax
    setg al
    movzx eax, al
    cmp eax, 0 ; comparar la condicion de bucle while
    je L1930269441152_end ; terninar el bucle si la condicion es falsa
    mov eax, [valor] ; cargar variable valor
    push eax; guardar en la pila
    mov eax, 1 ; cargar entero 1
    pop ebx; recuperar el primer operando
    sub ebx, eax; ebx = ebx - eax
    mov eax, ebx; eax = ebx
    mov [valor], eax ; asignar a valor
    jmp L1930269441152_start ; volvar al inicio del bucle while
L1930269441152_end: ; fin de bucle while
    mov eax, 0 ; cargar entero 0
    mov [i], eax ; asignar a i
L1930269441776_start: ; inicio del bucle for
    mov eax, [i] ; cargar variable i
    push eax
    mov eax, 1 ; cargar entero 1
    pop ebx
    cmp ebx, eax
    setle al
    movzx eax, al
    cmp eax, 0 ; comparar la condicion del for
    je L1930269441776_end ; salir del bucle si la condicion es falsa
    mov eax, [valor] ; cargar variable valor
    push eax; guardar en la pila
    mov eax, 1 ; cargar entero 1
    pop ebx; recuperar el primer operando
    add eax, ebx ; eax = eax + ebx
    mov [valor], eax ; asignar a valor
    mov eax, [i]
    add eax, 1
    mov [i], eax  ; i++
    jmp L1930269441776_start ; volver al inicio del bucle for
L1930269441776_end: ; fin del bucle for

    mov [resultado_condicional], eax ; asignar a resultado_condicional

    mov [circunferencia], eax ; asignar a circunferencia
    mov eax, [resultado_condicional] ; cargar variable resultado_condicional
    mov [temp_int], eax ; asignar a temp_int
    mov eax, [circunferencia] ; cargar variable circunferencia
    mov [temp_float], eax ; asignar a temp_float
    mov eax, 0 ; cargar entero 0
    ret ; retorno desde la subrutina
    mov esp, ebp
    pop ebp
    ret


