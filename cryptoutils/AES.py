from Crypto.Cipher import AES
import binascii

def padPKCS7(s, size):
	pad = size - len(s)%size
	if pad == 0 :
		return s + bytes([size] * size)
	return s + bytes([pad] * pad)

class Error(Exception):
	pass

class BadPaddingError(Error):
	pass


def stripPKCS7(s,size=16):
	
	padding_len = s[-1]

	if padding_len > size or padding_len == 0x00:
		#print(s)
		raise BadPaddingError

	slen = len(s)
	padding = s[slen - padding_len:slen]
	for x in padding:
		if x != padding_len:
			#print(s)
			raise BadPaddingError
	
	return s[:slen-padding_len]


def ecb_encrypt(s,key):
	size = len(key)
	s = padPKCS7(s,size)
	
	blocks = get_blocks(s,size)
	
	cipher = AES.new(key,AES.MODE_ECB)
	
	cipherText = b''
	for i in range(len(blocks)):
		cipherText = cipherText + cipher.encrypt(blocks[i])

	return cipherText	

def ecb_decrypt(s,key):
	
	size = len(key)
	cipherBlocks = get_blocks(s,size)
	
	cipher = AES.new(key, AES.MODE_ECB)

	plainText = b''
	for i in range(len(blocks)):
		plainText = plainText + cipher.decrypt(cipherBlocks[i])

	return plainText

def cbc_encrypt(s,k, iv=b''):

	cipher = AES.new(k, AES.MODE_ECB)
	size = len(k)
	x = padPKCS7(s,size)
	blocks = get_blocks(x, size)
	cipherBlocks = [None] * (len(blocks) + 1)
	cipherBlocks[0] = iv

	for i in range(len(blocks)):
		cipherBlocks[1+i] = cipher.encrypt(XORBlocks(blocks[i], cipherBlocks[i]))

	cipherText = b''
	for i in range(len(blocks)):
		cipherText += cipherBlocks[1+i]

	return cipherText	

def cbc_decrypt(y,k, iv=b''):
	cipher = AES.new(k, AES.MODE_ECB)
	size = len(k)
	blocks = get_blocks(y, size)
	plainBlocks = [None] * len(blocks)

	plainBlocks[0] = XORBlocks(iv, cipher.decrypt(blocks[0]))

	for i in range(1,len(blocks)):
		plainBlocks[i] = XORBlocks(blocks[i-1], cipher.decrypt(blocks[i]))

	plainText = b''
	for i in range(len(blocks)):
		plainText += plainBlocks[i]
	
	return stripPKCS7(plainText,size)

def XORBlocks(b1,b2):
	return bytes([x^y for x,y in zip(b1,b2)])

def get_blocks(s, blocksize=16):
	return [s[i:i+blocksize] for i in range(0, len(s), blocksize)]

def union_blocks(blocks):
	out = b''
	for b in blocks:
		out += b

	return out
	
def ctr_encrypt(s, key, nonce,size=16):

    nonce = nonce.to_bytes(8,byteorder='little')
    keystream = bytes()
    block_count = 0
    while len(keystream) <= len(s):
        block = nonce + block_count.to_bytes(8, byteorder='little')
        keystream += AES.ecb_encrypt(block, key)[:size]
        block_count += 1
    return XORBytes(keystream, s)

def ctr_decrypt(s,key,nonce):
    return ctr_encrypt(s,key,nonce)

def XORBytes(s1,s2):
    out = b''
    for b1,b2 in zip(s1,s2):
        out += bytes([b1^b2])
    return out

def test_ctr():
    base64 = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='
    data = binascii.a2b_base64(base64)

    print(ctr_decrypt(data, "YELLOW SUBMARINE",0))



def main():
	test_padding()
	test_cbc()
	s = b'a'*16 + b'b'*16 + b'c'*16 + b'd'*16
	print(s == union_blocks(get_blocks(s)))
	test_ctr()

def test_cbc():
	s = b'abcd' * 4 * 10 + b'a'
	iv = b'\x42\x43\x44\x45\x42\x43\x44\x45\x42\x43\x44\x45\x42\x43\x44\x45' 
	key = iv
	y = cbc_encrypt(s,key,iv)
	x = cbc_decrypt(y,key,iv)
	print(x)


def test_padding():
	s = b'ICE ICE BABY'
	x = padPKCS7(s,16)
	assert(stripPKCS7(x) == b'ICE ICE BABY')

	s = b'a'*16
	spad = s + b'\x10' * 16
	x = padPKCS7(s,16)
	assert(x == spad)
	assert(stripPKCS7(x) == s)

	bad1 = b'ICE ICE BABY\x05\x05\x05\x05'
	bad2 = b'ICE ICE BABY\x01\x02\x03\x04'

	try:
		stripPKCS7(bad1,16)
	except BadPaddingError:
		pass
	try:
		stripPKCS7(bad2,16)
	except BadPaddingError:
		pass

	

	print("PaddingTest Passed")
	return True

#main()
