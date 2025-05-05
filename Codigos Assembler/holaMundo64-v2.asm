; Hola mundo version 64 bits
; nasm -f elf64 holaMundo64-v2.asm -o holaMundo64-v2.o
; ld -0 holaMundo64-v2 holaMundo64-v2.o

%include	"stdio64.asm"
SECTION .data
	msg	db	"Hola mundo", 10, 0

SECTION .text
	global _start

_start:
	mov rax, msg
	call printStr
	
	call salir
