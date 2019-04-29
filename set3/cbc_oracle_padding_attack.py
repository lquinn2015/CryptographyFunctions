import sys
sys.path.append('../cryptoutils/')

import AES
import numpy.random as rand
import binascii

key = rand.bytes(16)
iv = rand.bytes(16)

plain_texts = [b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=', b'MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=', b'MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==', b'MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==', b'MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl', b'MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==', b'MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==', b'MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=', b'MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=', b'MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93']

plains = [binascii.a2b_base64(p) for p in plain_texts]


def get_cbc_cipher():
	target = rand.randint(10)
	return AES.cbc_encrypt(plains[target],  key, iv)


# this can only tell us if we have passed or failed the padding
def validate_decryption(s):	
	try:
		AES.cbc_decrypt(s,key,iv)
	except AES.BadPaddingError:
		return False
	return True


"""
	We know all Ci terms

	CBC   	E(P1)  -> IM1 + IV = C1
			E(P2)  -> IM2 + C1 = C2
			E(P3)  -> IM3 + C2 = C3
			
	We can get all but IM1 but providing Ci' blocks and checking for valid padding

"""

def solve_block(s_block, a_block):
	
	IM = b'\x00' * 16
	padding = 0
	for i in reversed(range(16)):
		padding += 1

		a = a_block
		a = setup_ablock(a, IM, i, padding,16)
		
		sols = []
		for b in range(1,255): 
			a = idxBytes(a, i, b)
			cnew = AES.union_blocks([a,s_block])
			if validate_decryption(cnew):
				sols.append(b)
				#IM = idxBytes(IM, i, padding ^ b)
		if len(sols) == 1:
			IM = idxBytes(IM, i, padding ^ sols[0])
		else:
			for b in sols:
				a = a_block
				a = idxBytes(a,i,b)
				a = idxBytes(a,i-1,b)			
				cnew = AES.union_blocks([a,s_block])
				if validate_decryption(cnew):
					IM = idxBytes(IM, i, padding ^ b)
			if IM[i] == 0:
				IM = idxBytes(IM, i, padding)
				

	return AES.XORBlocks(IM, a_block)

def setup_ablock(a_block, IM, solved, target_pad, size=16):


	solved += 1
	while solved < size:
		a_block = idxBytes(a_block, solved, target_pad ^ IM[solved])
		# P = C ^ IM/ we want  P = target thus let C = IM ^ target
		solved += 1
	return a_block


def idxBytes(s,i,x):
	return s[:i] + bytes([x]) + s[i+1:]



def gen_padding(num, size=16):	
	return bytes([0]*(size-num)) + bytes([num]*num)


def main():

	for texts in plains:
		texts = iv + texts
		cipher = AES.cbc_encrypt(texts,  key, iv)
		blocks = AES.get_blocks(cipher)
		break_cipher(blocks)




def break_cipher(blocks):
	nblock = []

	for i in reversed(range(1,len(blocks))):
		nblock.append( solve_block(blocks[i], blocks[i-1]))
	print(AES.union_blocks(reversed(nblock)))


main()
