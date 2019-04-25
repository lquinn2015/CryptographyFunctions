from Crypto.Cipher import AES
import binascii



def encrypt(s,key):
	assert(len(key) % 16 == 0)
	assert(len(s) % len(key) == 0)

	cipher = AES.new(key,AES.MODE_ECB)
	return cipher.encrypt(s)

def decrypt(s,key):
	assert(len(key) % 16 == 0)
	assert(len(s) % len(key) == 0)

	cipher = AES.new(key,AES.MODE_ECB)
	return cipher.decrypt(s)


def main():
	
	f = open('7.txt', 'r')
	base64 = f.read().strip('\n')
	data = binascii.a2b_base64(base64)

	key = b'YELLOW SUBMARINE'
	cipher = AES.new(key, AES.MODE_ECB)
	msg = cipher.decrypt(data)
	print(msg.decode())

main()
