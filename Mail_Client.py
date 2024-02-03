import smtplib
import sys
import time
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase  
from email.mime.multipart import MIMEMultipart
def email_func():
    lines = []
    server_dict = {'gmail': 'smtp.gmail.com', 'outlook': 'smtp-mail.outlook.com', 'yahoo': 'smtp.mail.yahoo.com', 'proton': 'smtp.protonmail.ch', 'protonmail': 'smtp.protonmail.ch'}
    from_email = input("Enter sender's email address: ")
    decide = from_email.split("@")
    server_decide = decide[1].split(".") 
    serve = server_decide[0]
    if serve in server_dict.keys():
        server = server_dict[serve]  
    else:
        print("Email provider not supported currently")  
        time.sleep(2)
        sys.exit()
    password = input("Enter password: ")
    try:
        smtp = smtplib.SMTP(server , 587)
        status , response = smtp.ehlo()
        status , response = smtp.starttls()
        print(f"Status message: {response}")
        status , response = smtp.login(from_email , password)
        print(f"Status message: {response}")
    except OSError as e:
        print(f"Error occured: {e}")
        time.sleep(2)
        sys.exit()
    to_email = input("Enter reciever's email address: ")
    sub = input("Enter subject: ")
    print("Enter body: ")
    while True:
        user = input()
        if user == "":
            break
        else:
            lines.append(user + "\n")
    message = ''.join(lines)
    opt = input("Enter 'Y' for attaching files , 'N' to send only text: ")
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = sub
    msg.attach(MIMEText(message , "plain"))
    if opt == "Y":
        number = int(input("Enter number of attachments: "))
        try:
            for i in range(0 , number):
                    filename_ = input("Enter file name: ")
                    file = open(filename_ , "rb")
                    p = MIMEBase("application" , "octet-stream")
                    p.set_payload(file.read())
                    encoders.encode_base64(p)
                    p.add_header("content-disposition" , "attachment" , filename = filename_)
                    msg.attach(p)
                    print(f"{filename_} attached successfully")
        except OSError as e:
            print(f"Error occurred: {e}")
            time.sleep(2)
            sys.exit()
        text = msg.as_string()
        smtp.sendmail(from_email , to_email , text)
        print(f"Mail sent to {to_email}")
    elif opt == "N":
        txt1 = msg.as_string()
        smtp.sendmail(from_email , to_email , txt1)
        print(f"Mail sent to {to_email}")
    else:
        print("Enter appropriate option")
    time.sleep(2)
    smtp.quit()
if __name__ == "__main__":
    email_func()