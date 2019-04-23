import binascii
import math

def hex2bytes(string):
    return bytearray.fromhex(string)

def bytes2hex(arr):
    return binascii.hexlify(arr)

def shannonEntropy(string):
    probs = [float(string.count(c)/len(string)) for c in dict.fromkeys(list(string))]
    entropy = - sum([p*math.log(p) / math.log(2.0) for p in prob])
    return entropy

alphabet = "abcdefghijklmnopqrstuvwxyz "

englishLetterFreq = {'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07}
englishFreqWithSpaces = {'a':0.0651738, 'b':0.0124248, 'c': 0.0217339, 'd': 0.0349835, 'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610, 'h': 0.0492888, 'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490, 'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302, 'p': 0.0137645, 'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357, 'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692, 'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182}

def isTextOrSpace(c):
    c = ord(c)
    return (c >= ord('a') and c <= ord('z')) or (c >= ord('A') and c <= ord('Z')) or c == ord(' ')

def isPrintable(c):
    c = ord(c)
    return ord(' ') <= c and c < ord('~')

def Chi2ScoringFBytesArray(arr):
    return Chi2ScoringFString(arr.decode())

def Chi2ScoringFString(string):

    freq = []
    totalCount = 0
    string = string.lower()

    for c in alphabet:
        freq.append(float(string.count(c)))
        totalCount += freq[-1]
    chiScore = 0.0 
    for i,c in enumerate(alphabet):
        freq[i] = freq[i]/(totalCount+1)
        chiScore += ((freq[i] - englishFreqWithSpaces[i]) ** 2) / englishFreqWithSpaces[i]

    return chiScore



def PrintScoreBytesArray(arr):
    return TextScoreString(arr.decode())

def PrintScoreString(string):
   
    score = 0    
    for c in string:
        if isTextOrSpace(c):
            score += 1
        if isPrintable(c):
            score += 1
    return (score/len(string))/2  # returns between 0-1

ciphertext = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
