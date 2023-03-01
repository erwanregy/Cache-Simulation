crc: crc_32.c Makefile
	gcc -static crc_32.c -O3 -o crc 

crc.arm: crc_32 Makefile
	arm-linux-gnueabi-gcc -static crc_32.c -O3 -o crc.arm

clean:
	rm -rf crc crc.arm output*
