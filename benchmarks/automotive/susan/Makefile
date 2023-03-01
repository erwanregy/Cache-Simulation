susan: susan.c Makefile
	gcc -static -O4 -o susan susan.c -lm 

susan.arm: susan.c Makefile
	arm-linux-gnueabi-gcc -static -O4 -o susan.arm susan.c -lm

clean:
	rm -rf susan susan.arm output*
