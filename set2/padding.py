

def padPKCS7(s, size):
	length = size - len(s)%size
	s += bytes([length]*length)
	return s

def main():

	s = b'Yellow Submarine'
	print(padPKCS7(s,20))
	
#main()
