import sys
sys.path.append('../cryptoutils')

import AES
import numpy.random as rand

def encryption_orcale(s):
	prob = rand.random(1)
	
	key = rand.bytes(16)
	out = b''
	ans = ''
	if prob > .5:
		out = AES.ecb_encrypt(s,key)
		ans = 'ecb'	
	else:
		out = AES.cbc_encrypt(s,key)
		ans = 'cbc'
	return out, ans

def guessMode(s):
	
	blocks = AES.get_blocks(s,16)
	uniq = set(b for b in blocks)
	if len(uniq) != len(blocks):
		return 'ecb'
	else:
		return 'cbc'
	

def main():
	
	for i in range(100):
		s = b'\x42' * 16 * 30
		out, ans = encryption_orcale(s)
		assert(guessMode(out) == ans)
	
	print("Winning")
		

#main()	
