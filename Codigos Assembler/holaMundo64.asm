; Hola mundo version 64 bits
; nasm -f elf64 holaMundo64.asm -o holaMundo64.o
; ld -0 holaMundo64 holaMundo64.o

SECTION .data
	msg	db	"Hola mundo", 10

SECTION .text
	global _start

_start:
	mov	rdx, 12		; longitud de cadena y rdx por ser de 64 bits
	mov	rsi, msg	; apuntamos a direccion de inicio de la cadena
	mov	rdi, 1		; stdout, standar output
	mov	rax, 1
	syscall

	mov	rax, 60
	xor	rdi, rdi
	syscall
