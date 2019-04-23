import codecs

def hex2base64(hexstr):
    return codecs.encode(codecs.decode(hexstr.hex(), 'hex'), 'base64').decode()

def main():
    instr = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    binstr = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
    bytes2 = bytearray.fromhex(binstr)
    print(bytes2)
    bytesObj = bytearray(codecs.decode(instr, 'hex'))
    base64 = hex2base64(bytesObj)
    print(base64)
main()
