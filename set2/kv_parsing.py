import numpy.random as rand
import sys
sys.path.append('../cryptoutils')
import AES
import binascii

key = rand.bytes(16)


def kv2dict(kv):


	model = dict()
	elements = kv.split('&')

	for elem in elements:
		p = elem.split('=')
		model[p[0]] = p[1]

	return model

def encodeDict(model):

	s = ''

	for x in model.keys():
		s = s + str(x) + '='  +model[x] + '&'
	return s[:-1]

def profile_for(s):

	s = s.strip('=').strip('&')
	model = dict()
	model['email'] = s
	model['uid'] = str(10) #  they actually wanted 10 here str(rand.randint(0,100))
	model['role'] = 'user'
	return encodeDict(model)

def oracle(acc):
	s = profile_for(acc)
	return AES.ecb_encrypt(s.encode(),key)



def main():

	desired_ciphertext = AES.ecb_encrypt(b'email=lue@gmail.com&uid=10&role=admin', key)

	attack_key = 'a'*10 + 'admin' + '\x0b' * 11
	out = oracle(attack_key)
	real = oracle('lue@gmail.com')
	real = real[:-16]
	ciphertext = real + out[16:32]
	print(ciphertext == desired_ciphertext)

main()	
