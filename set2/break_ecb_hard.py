import sys
sys.path.append('../cryptoutils/')

import AES
import binascii
import numpy.random as rand
import time

secret = binascii.a2b_base64('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgUm9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')
key = rand.bytes(16)
prefix_len = rand.randint(1,16)
prefix = rand.bytes(prefix_len)

def oracle(s):
	plain = prefix + s + secret
	return AES.ecb_encrypt(plain, key)


"""
	This is not a clean solution but it is a soultion i am proud of
	it doesn't break any assumptions (i guess i don't find block size but hey)
	it is a huge advancement over break_ecb
	
"""

def break_ecb():
	
	msg_len = len(oracle(b''))
	max_block = len(AES.get_blocks(oracle(b'')))
	pre_len = -1

	block_size = 16

	for i in range(block_size):
		s = b'a'*i
		pad = b'a'*block_size*2
		blocks = AES.get_blocks(oracle(s+pad))[0:3]
		
		if len(blocks) != len(set(blocks)):
			pre_len = block_size-i
			break


	known = b''
	curr_block = 1
	for fake_pad in reversed(range(block_size)):
		pad = b'a' * fake_pad
		blocks = AES.get_blocks(oracle(s+pad))
		for i in range(255):
			pad2 = b'a' * fake_pad + known + bytes([i])
			cblocks = AES.get_blocks(oracle(s + pad2))
			if cblocks[curr_block] == blocks[curr_block]:
				known += bytes([i])
				print(known)
				break

		
	solved = block_size
	curr_block = 2
	while solved < msg_len and curr_block <= max_block :
		for fake_pad in reversed(range(16)):
			pad = b'a'*fake_pad
			blocks = AES.get_blocks(oracle(s+pad))

			for i in range(255):
				pad2 = known[solved-block_size+1:solved+1] + bytes([i])
				cblocks = AES.get_blocks(oracle(s+pad2))
				if cblocks[1] == blocks[curr_block]:
					known += bytes([i])
					solved+=1
					print(known)
					break
		curr_block += 1
		
				
	print(known.decode())	



def main():
	break_ecb()


main()

