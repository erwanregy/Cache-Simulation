test: test.c
	gcc -static -Ofast test.c -o test

test.arm: test.c
	arm-linux-gnueabi-gcc -static -Ofast test.c -o test.arm

clean:
	rm test test.arm
