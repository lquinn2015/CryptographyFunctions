import sys
sys.path.append('../cryptoutils/')
sys.path.append('../set1/')
import AES
import binascii
import numpy.random as rand

import single_byte_xor as sbx

# we can do better but i don't think putting in the manual labor for tuning is worth it at this time


base64s = ['SSBoYXZlIG1ldCB0aGVtIGF0IGNsb3NlIG9mIGRheQ==', 'Q29taW5nIHdpdGggdml2aWQgZmFjZXM=','RnJvbSBjb3VudGVyIG9yIGRlc2sgYW1vbmcgZ3JleQ==','RWlnaHRlZW50aC1jZW50dXJ5IGhvdXNlcy4=','SSBoYXZlIHBhc3NlZCB3aXRoIGEgbm9kIG9mIHRoZSBoZWFk','T3IgcG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==','T3IgaGF2ZSBsaW5nZXJlZCBhd2hpbGUgYW5kIHNhaWQ=','UG9saXRlIG1lYW5pbmdsZXNzIHdvcmRzLA==','QW5kIHRob3VnaHQgYmVmb3JlIEkgaGFkIGRvbmU=','T2YgYSBtb2NraW5nIHRhbGUgb3IgYSBnaWJl','VG8gcGxlYXNlIGEgY29tcGFuaW9u','QXJvdW5kIHRoZSBmaXJlIGF0IHRoZSBjbHViLA==','QmVpbmcgY2VydGFpbiB0aGF0IHRoZXkgYW5kIEk=','QnV0IGxpdmVkIHdoZXJlIG1vdGxleSBpcyB3b3JuOg==','QWxsIGNoYW5nZWQsIGNoYW5nZWQgdXR0ZXJseTo=','QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=','VGhhdCB3b21hbidzIGRheXMgd2VyZSBzcGVudA==','SW4gaWdub3JhbnQgZ29vZCB3aWxsLA==','SGVyIG5pZ2h0cyBpbiBhcmd1bWVudA==','VW50aWwgaGVyIHZvaWNlIGdyZXcgc2hyaWxsLg==','V2hhdCB2b2ljZSBtb3JlIHN3ZWV0IHRoYW4gaGVycw==','V2hlbiB5b3VuZyBhbmQgYmVhdXRpZnVsLA==','U2hlIHJvZGUgdG8gaGFycmllcnM/','VGhpcyBtYW4gaGFkIGtlcHQgYSBzY2hvb2w=','QW5kIHJvZGUgb3VyIHdpbmdlZCBob3JzZS4=','VGhpcyBvdGhlciBoaXMgaGVscGVyIGFuZCBmcmllbmQ=','V2FzIGNvbWluZyBpbnRvIGhpcyBmb3JjZTs=','SGUgbWlnaHQgaGF2ZSB3b24gZmFtZSBpbiB0aGUgZW5kLA==','U28gc2Vuc2l0aXZlIGhpcyBuYXR1cmUgc2VlbWVkLA==','U28gZGFyaW5nIGFuZCBzd2VldCBoaXMgdGhvdWdodC4=','VGhpcyBvdGhlciBtYW4gSSBoYWQgZHJlYW1lZA==','QSBkcnVua2VuLCB2YWluLWdsb3Jpb3VzIGxvdXQu','SGUgaGFkIGRvbmUgbW9zdCBiaXR0ZXIgd3Jvbmc=','VG8gc29tZSB3aG8gYXJlIG5lYXIgbXkgaGVhcnQs','WWV0IEkgbnVtYmVyIGhpbSBpbiB0aGUgc29uZzs=','SGUsIHRvbywgaGFzIHJlc2lnbmVkIGhpcyBwYXJ0','SW4gdGhlIGNhc3VhbCBjb21lZHk7','SGUsIHRvbywgaGFzIGJlZW4gY2hhbmdlZCBpbiBoaXMgdHVybiw=','VHJhbnNmb3JtZWQgdXR0ZXJseTo=','QSB0ZXJyaWJsZSBiZWF1dHkgaXMgYm9ybi4=']

plains = [binascii.a2b_base64(f) for f in base64s]

nonce = 0
key = rand.bytes(16)

ciphers = [AES.ctr_encrypt(f,key, nonce) for f in plains]

def break_CTR_repeated_nonce():

	max_len = min(len(f) for f in ciphers) # xor length is this

	clipped_ciphers = [f[0:max_len] for f in ciphers]

	s = b''.join(clipped_ciphers)
	
	
	plains = AES.get_blocks(BreakRepeatedXOR(s, max_len).encode(),max_len)


	return plains
	

def BreakRepeatedXOR(s, keysize):
    blocks = [s[i::keysize] for i in range(0,keysize)]
    decrypt_blocks = []
    key = ""
    for b in blocks:
        block, key_bit = sbx.breakXORAndKey(b)
        key += key_bit
        decrypt_blocks.append(block)

    out = ""
    for i in range(len(s)):
        x = i % len(decrypt_blocks)
        y = int(i / len(decrypt_blocks))
        out = out +  decrypt_blocks[x][y]

    return out, key

def main():
	plain, key = break_CTR_repeated_nonce()
	

main()







