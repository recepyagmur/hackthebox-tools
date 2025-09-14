import base64


enc_password = "0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E"
key = "armando"
encode_key= key.encode()

array=base64.b64decode(enc_password)

array2= bytearray(len(array))

for i in range(len(array)):
    array2[i]=array[i] ^ encode_key[i % len(encode_key)] ^ 223


password = array2.decode()
print(password)


