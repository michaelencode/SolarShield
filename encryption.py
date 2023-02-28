from cryptography.fernet import Fernet

key="welovebeerandbeach"

def encry(passcode):
    fernet=Fernet(key)
    encMessage=fernet.encrypt(passcode.encode())
    return encMessage

def decry(depasscode):
    fernet=Fernet(key)
    decMessage=fernet.decrypt(depasscode).decode()
    return decMessage
a="123456789"
print (encry(a))