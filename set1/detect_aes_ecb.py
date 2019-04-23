import itertools
import binascii


def detect_ecb(s,klen):
	
	blocks = [s[i:i+klen] for i in range(0,len(s),klen)]
	pairs = itertools.combinations(blocks,2)
	
	score = 0
	for p in pairs:
		if p[0] == p[1]:
			score += 1
	return score > 0


def main():
	
	f = open('8.txt', 'r')
	data = f.read()
	lines = data.split('\n')

	for i,l in enumerate(lines):
		if detect_ecb(binascii.unhexlify(l), 16):
			print("Possible AES ECB mode on line: " + str(i))
			



main()
