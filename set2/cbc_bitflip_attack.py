import sys
sys.path.append('../cryptoutils/')

import AES
import binascii
import numpy.random as rand

key = rand.bytes(16)
iv = rand.bytes(16)


def escape(s):
	return s.replace(b'%',b'%37').replace(b';', b'%59').replace(b'=',b'%61')

def escape(s):
	return s.replace(b'%37',b'%').replace(b'%59',b';').replace(b'%61', b'=')

def oracle(s):
	c1 = b'comment1=cooking%20MCs;userdata='
	c2 = b';comment2=%20like%20a%20pound%20of%20bacon'
	f = c1+escape(s)+c2

	return AES.cbc_encrypt(f, key, iv)

def is_admin(s):
	s2 = AES.cbc_decrypt(s,key,iv)
	params = s2.split(b';')
	for p in params:
		comps = p.split(b'=')
		if comps[0] == b'admin' and comps[1] == b'true':
			return True
	return False

def get_padding(max_size):

	x = [len(oracle(b'a'*i)) for i in range(max_size)]
	olen = x[0]
	for i,t in enumerate(x):
		if t > olen: 
			return i-1
	

def turn_admin():

	#size = get_padding(32)	
	# assumption is that i known i am ecnrypting the comment 1 strings
	blocks = AES.get_blocks(oracle(b'a'*16))
	c2 = b';comment2=%20like%20a%20pound%20of%20bacon'
	admin = b';admin=true;0000'
	delta_plain = AES.XORBlocks(admin, c2[:16])
	add_this = AES.XORBlocks(blocks[2],delta_plain)
	blocks[2] = add_this
	
	ncipher = b''
	for b in blocks:
		ncipher = ncipher + b

	print(is_admin(ncipher))


def main():
	turn_admin()

main()
