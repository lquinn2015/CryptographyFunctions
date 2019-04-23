
import cryptoutil as cy

def XORHexStr(a,b):
    hex1 = cy.hex2bytes(a)
    hex2 = cy.hex2bytes(b)
    out  = bytearray()
    for x in zip(hex1,hex2):
        out.append(x[0] ^ x[1])
    return out


def main():
    message = '1c0111001f010100061a024b53535009181c'
    key = '686974207468652062756c6c277320657965'

    y = XORHexStr(message,key) # output as bytesarray object
    print(y)
    print(cy.bytes2hex(y))
  
#main()  
    
