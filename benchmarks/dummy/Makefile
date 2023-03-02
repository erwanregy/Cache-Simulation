dummy: dummy.c
	gcc -static -Ofast dummy.c -o dummy

dummy.arm: dummy.c
	arm-linux-gnueabi-gcc -static -Ofast dummy.c -o dummy.arm

clean:
	rm dummy dummy.arm
