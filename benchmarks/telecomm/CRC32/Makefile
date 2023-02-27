x86: crc_32.c Makefile
	gcc -static crc_32.c -O3 -o crc 

arm: crc_32.c Makefile
	arm-linux-gnueabihf-gcc -static crc_32.c -O3 -o crc-arm

clean:
	rm -rf crc crc-arm output*
