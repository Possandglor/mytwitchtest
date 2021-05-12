import random
import socket
import io
import time
import os

alphabet = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"

text = ""
for i in range(150000):
    text+= alphabet[random.randint(1,len(alphabet)-1)]

dir = os.path.abspath(os.curdir)
with open(dir+'/config/randomtext.txt','w+') as f:
    f.write(text)
