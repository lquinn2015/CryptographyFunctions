import sys
sys.path.append('../cryptoutils/')
import AES
import binascii

def ctr_encrypt(s, key, nonce,size=16):

	nonce = nonce.to_bytes(8,byteorder='little')
	keystream = bytes()
	block_count = 0
	while len(keystream) <= len(s):
		block = nonce + block_count.to_bytes(8, byteorder='little')	
		keystream += AES.ecb_encrypt(block, key)[:size]
		block_count += 1
	return XORBytes(keystream, s)

def ctr_decrypt(s,key,nonce):
	return ctr_encrypt(s,key,nonce)

def XORBytes(s1,s2):
	out = b''
	for b1,b2 in zip(s1,s2):
		out += bytes([b1^b2])
	return out

def test_ctr():
	base64 = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
	data = binascii.a2b_base64(base64)

	print(ctr_decrypt(data, "YELLOW SUBMARINE",0))

test_ctr()
