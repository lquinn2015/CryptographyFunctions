from Crypto.Cipher import AES
import binascii



def main():
	
	f = open('7.txt', 'r')
	base64 = f.read().strip('\n')
	data = binascii.a2b_base64(base64)

	key = b'YELLOW SUBMARINE'
	cipher = AES.new(key, AES.MODE_ECB)
	msg = cipher.decrypt(data)
	print(msg.decode())

main()
