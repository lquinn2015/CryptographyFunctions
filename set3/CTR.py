import sys
sys.path.append('../cryptoutils/')
import AES
import binascii

base64 = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
data = binascii.a2b_base64(base64)


def ctr_encrypt(s, key, nonce):

	keystream = b''
	needed_key = len(s)
	
	AES.ecb_encrypt(nonce)
