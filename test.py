from Crypto.Cipher import DES
obj=DES.new('abcdefgh', DES.MODE_ECB)
plain="Guido van Rossum is a space alien."
#obj.encrypt(plain)

pad = '&' * (8-(len(plain) % 8))
print(pad)

ciph=obj.encrypt(plain+pad)

print( ciph ) 

print( obj.decrypt(ciph).decode("utf-8").strip('&') )
