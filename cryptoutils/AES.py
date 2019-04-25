from Crypto.Cipher import AES
import binascii

def padPKCS7(s, size):
	pad = size - len(s)%size
	if pad == 0 or pad == 16:
		return s
	return s + bytes([pad]* pad) 

def ecb_encrypt(s,key):
	size = len(key)
	s = padPKCS7(s,size)
	
	blocks = get_blocks(s,size)
	
	cipher = AES.new(key,AES.MODE_ECB)
	
	cipherText = b''
	for i in range(len(blocks)):
		cipherText = cipherText + cipher.encrypt(blocks[i])

	return cipherText	

def ecb_decrypt(s,key):
	
	size = len(key)
	cipherBlocks = get_blocks(s,size)
	
	cipher = AES.new(key, AES.MODE_ECB)

	plainText = b''
	for i in range(len(blocks)):
		plainText = plainText + cipher.decrypt(cipherBlocks[i])

	return plainText

def cbc_encrypt(s,k, iv=b''):

	cipher = AES.new(k, AES.MODE_ECB)
	size = len(k)
	x = padPKCS7(s,size)
	blocks = get_blocks(x, size)
	cipherBlocks = [None] * (len(blocks) + 1)
	cipherBlocks[0] = iv

	for i in range(len(blocks)):
		cipherBlocks[1+i] = cipher.encrypt(XORBlocks(blocks[i], cipherBlocks[i]))

	cipherText = b''
	for i in range(len(blocks)):
		cipherText += cipherBlocks[1+i]

	return cipherText	

def cbc_decrypt(y,k, iv=b''):
	cipher = AES.new(k, AES.MODE_ECB)
	size = len(k)
	blocks = get_blocks(y, size)
	plainBlocks = [None] * len(blocks)

	plainBlocks[0] = XORBlocks(iv, cipher.decrypt(blocks[0]))

	for i in range(1,len(blocks)):
		plainBlocks[i] = XORBlocks(blocks[i-1], cipher.decrypt(blocks[i]))

	plainText = b''
	for i in range(len(blocks)):
		plainText += plainBlocks[i]

	return plainText

def XORBlocks(b1,b2):
	return bytes([x^y for x,y in zip(b1,b2)])

def get_blocks(s, blocksize=16):
	return [s[i:i+blocksize] for i in range(0, len(s), blocksize)]

def main():
	s = b'abcd' * 4 * 10 + b'a'
	iv = b'\x42\x43\x44\x45\x42\x43\x44\x45\x42\x43\x44\x45\x42\x43\x44\x45' 
	key = iv
	y = cbc_encrypt(s,key,iv)
	x = cbc_decrypt(y,key,iv)

#main()
