import sys
sys.path.append('../cryptoutils')

import AES
import numpy.random as rand
import binascii
import time


def encryption_oracle(s, key):
    prob = rand.random(1)

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


def oracle(s1,s2,key):
	plain = s1 + s2

	out = ''
	ans = 'no'
	while ans != 'ecb':
		out, ans = encryption_oracle(plain, key)
	return out

def find_block_size(s,key):
	
	initial = len(oracle(b'',s,key))
	for i in range(256):
		s1 = b'a' * i
		nsize = len(oracle(s1,s,key))
		if nsize != initial:
			return nsize - initial, i
	return -1

"""
 	Notes for refactoring make your orcale function only take a string it looks dumb that you give it the key and text
	You only use padding once to figure out the fise SIZE of bytes after that we know enough text to solve the rest

	This was my first write so its not horrible but there is a ton of room for improvement like in the next section
	I don't like python3 byte stuff its were compared to something like c or java but not having to implment AES is nice
"""
def crack_ecb(extra,key, size):

	list_of_bytes = b''	
	for i in range(255):
		list_of_bytes += bytes([i])
	
	original_cipher = oracle(b'',extra,key)
	num_blocks = len(AES.get_blocks(original_cipher, size))
	msg = b''
	curr_block = 0
	while curr_block < num_blocks:
		text = extra[curr_block*size:]
		known_text = b''
		for i in reversed(range(size)):
			pad = bytes(b'a'*i)
			one_unknown = pad + known_text + text
			cipher2 = oracle(b'',one_unknown, key)[0:16]
			for b in list_of_bytes:
				one_known = pad + known_text + bytes([b]) 
				sol = oracle(b'',one_known, key)
				if sol == cipher2:
					known_text += bytes([b])
					text = text[1:]
					break
		curr_block += 1
		msg += known_text	


	return msg

	"""

	for char in readable_bytes:
		plain = bytes([char] * size)
		cipher = oracle(plain,extra, key)
		known_block = AES.get_blocks(cipher, size)[0]
		for i in range(size):
			decryption_dicts[i][known_block[i]] = char
	
	originalCipher = oracle(b'',extra,key)
	decrypt = ''
	for i,b in enumerate(originalCipher):
		i = i % size
		if b in decryption_dicts[i]:
			decrypt += chr(decryption_dicts[i][b])
		else:
			decrypt += '*'

	return decrypt
	"""
def main():
	base64 = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
	extra = binascii.a2b_base64(base64)

	key = rand.bytes(16)
	block_size,bytes_to_next_block = find_block_size(extra,key)

	plain = crack_ecb(extra,key,block_size)  # it has the key and data only to run the ecb stuff
	print(plain)


main()
