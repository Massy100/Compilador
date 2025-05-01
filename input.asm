; Lectura de datos desde teclado y almacenamiento en memoria

%include 'stdio.asm'

SECTION .data
	msg1	db	'Ingrese su nombre:', 0
	msg2	db	'Hola ', 0

SECTION .bss
	nombre	resb	20

SECTION .text
	global _start

_start:
	mov	eax, msg1
	call	printstr

	mov	edx, 20			; edx = espacio total para lectura
	mov	ecx, nombre		; direccion de memoria para almacenar lo que se lea
	mov	ebx, 0			; Lee desde STDIN
	mov	eax, 3			; Funcion de lectura del teclado SYS_READ
	int	80h

	mov	eax, msg2
	call 	printstr
	
	mov 	eax, nombre
	call	printstr

	call	quit
