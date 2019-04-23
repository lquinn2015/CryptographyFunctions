import binascii as bin
import time


def CyclicXOR(string, keyArr):
	
	out = b''
	i = 0
	for c in string:
		n = chr(c^keyArr[i]).encode()
		out = out + n
		i = (i+1) % len(keyArr)

	return out

def main():

	message = b'Burning \'em, if you ain\'t quick and nimble\nI go crazy when I hear a cymbal'

	key = [ord(c) for c in "ICE"]

	y = CyclicXOR(message, key)
	print(bin.hexlify(y))



main()
