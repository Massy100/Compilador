nasm -f elf32 programa.s -o programa.o  
gcc -m32 programa.o -o programa         
./programa  