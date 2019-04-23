import binascii
import time
import itertools
import single_byte_xor as sbx

def HammingDistance(s1,s2):
	dist = 0
	for x in zip(s1,s2):
		bitDiff = x[0]^x[1]
		binary = bin(bitDiff)
		bits = [ones for ones in binary[2:] if ones=='1']
		dist += len(bits)
	return dist

def FindKeySize(s):
	
	max_size = 40

	best_score = float('inf')
	best_size = -1

	for size in range(2,max_size+1):
		blocks = [s[i:i+size] for i in range(0, len(s), size)][0:4]
		pairs = list(itertools.combinations(blocks,2))
		scores = [HammingDistance(p[0],p[1])/float(size) for p in pairs]
		score = sum(scores) / len(scores)
		if score < best_score:
			best_score = score
			best_size = size
	return best_size
	
def BreakRepeatedXOR(s, keysize):
	blocks = [s[i::keysize] for i in range(0,keysize)]
	decrypt_blocks = []
	key = ""
	for b in blocks:
		block, key_bit = sbx.breakXORAndKey(b)
		key += key_bit
		decrypt_blocks.append(block)

	print("Found key was: " + str(key))
	out = ""  
	for i in range(len(s)):
		x = i % len(decrypt_blocks)
		y = int(i / len(decrypt_blocks))
		out = out +  decrypt_blocks[x][y]
	
	return out

def main():
	
	f = open('6.txt', 'r')
	data = f.read()
	base64 = data.strip('\n')
	s = binascii.a2b_base64(base64)
	keysize = FindKeySize(s)
	print(keysize)

	print(BreakRepeatedXOR(s, keysize))
	
	

def tests():
	s1 = b'this is a test'
	s2 = b'wokka wokka!!!'
	assert(HammingDistance(s1,s2) == 37)

main()
