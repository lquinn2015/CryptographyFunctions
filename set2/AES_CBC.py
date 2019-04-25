from Crypto.Cipher import AES
import binascii

def encrypt(x,k, iv=b''):
	assert(len(k) % 16 == 0)
	assert(len(x) % len(k) == 0)
	cipher = AES.new(k, AES.MODE_ECB)
	size = len(k)
	blocks = [x[i:i+size] for i in range(0, len(x), size)]

	cipherBlocks = [None] * (len(blocks) + 1)
	cipherBlocks[0] = iv

	for i in range(len(blocks)):
		cipherBlocks[1+i] = cipher.encrypt(XORBlocks(blocks[i], cipherBlocks[i]))
	
	cipherText = b''
	for i in range(len(blocks)):
		cipherText += cipherBlocks[1+i]

	return cipherText


def decrypt(y,k, iv=b''):
	assert(len(k) % 16 == 0)
	assert(len(y) % len(k) == 0)

	cipher = AES.new(k, AES.MODE_ECB)
	size = len(k)
	blocks = [y[i:i+size] for i in range(0, len(y), size)]
	plainBlocks = [None] * len(blocks)

	plainBlocks[0] = XORBlocks(iv, cipher.decrypt(blocks[0]))

	for i in range(1,len(blocks)):
		plainBlocks[i] = XORBlocks(blocks[i-1], cipher.decrypt(blocks[i]))
	
	plainText = b''
	for i in range(len(blocks)):
		plainText += plainBlocks[i]

	return plainText

def XORBlocks(b1,b2):
	out = b''
	for i in range(len(b1)):
		out += chr(ord(b1[i]) ^ ord(b2[i]))
	return out


def main():
	
	f = open('10.txt', 'r')
	base64 = f.read().strip('\n')
	data = binascii.a2b_base64(base64)

	iv = b'\x00' * 16
	k = b'YELLOW SUBMARINE'

	dout = decrypt(data,k,iv)
	dint = encrypt(dout, k, iv)
	print(dout)
	print("Encryption working: " + str(dint == data))

main()
