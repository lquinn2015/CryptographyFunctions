import cryptoutil as cy
import binascii as bin


def CyclicXOR(barr, keyArr):
    
	out = ""
	i = 0
	for b in barr:
		out +=  chr(b^keyArr[i])
		i = (i + 1) % len(keyArr)
	return out

def chi2score(s):

	s = s.lower()
	freq = cy.englishFreqWithSpaces
	alphabet = cy.alphabet
	total = 0
	chi = 0
	for c in alphabet:
		count = s.count(c)
		total += count
		probc = count/len(s)
		chi += ((probc-freq[c])**2)/freq[c]
	
	return 1/(chi + (-total + len(s)))

def freqScore(s):
	freq = cy.englishFreqWithSpaces
	score = 0
	for c in s.lower():
		if c in freq:
			score += freq[c]
	return score

def breakXOR(s):
	
	score = 0
	bestScore = 0
	best = ""
	for i in range(0,256):
		result = CyclicXOR(s, [i])
		#score = cy.Chi2ScoringFString(result)
		score = chi2score(result)
		if score > bestScore:
			bestScore = score
			best = result
	return best


def breakXORAndKey(s):
	
	score = 0
	bestScore = 0
	best = ""
	best_key = ""
	for i in range(0,256):
		result = CyclicXOR(s, [i])
		#score = cy.Chi2ScoringFString(result)
		score = chi2score(result)
		if score > bestScore:
			bestScore = score
			best = result
			best_key = i
	return best,chr(best_key)

def main():
    
	hexstr = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
	s = bin.unhexlify(hexstr)
	print(breakXOR(s))

#main()
