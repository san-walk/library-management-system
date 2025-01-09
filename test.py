import smtplib
from config import keys

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(keys.MAIL_USER, keys.MAIL_PASS)
    print("SMTP authentication successful")
    server.quit()
except smtplib.SMTPException as e:
    print(f"SMTP error: {e}")



'''
Date: 9th Jan 2025
Purpose: this file is used to check the debuging for the mail working
'''