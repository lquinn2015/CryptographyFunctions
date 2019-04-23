import single_byte_xor as sbx
import binascii as bin

def main():
	f = open("4.txt", "r")	
	lines = f.read()
	lines = lines.split("\n")
	score = 0
	best_score = 0
	winner = ""

	for l in lines:
		x = bin.unhexlify(l) 
		s = sbx.breakXOR(x)
		score = sbx.chi2score(s)
		#score = sbx.freqScore(s)
		
		if score >= best_score:
			best_score = score
			winner = s
	print(winner)

main()
