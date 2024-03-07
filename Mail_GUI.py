import tkinter as tk
from tkinter import StringVar , Toplevel , ttk , scrolledtext
from tkinter import filedialog as fd
import mysql.connector
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase  
from email.mime.multipart import MIMEMultipart
from Init_Mail import create_database

sender = ["Select sender's address"]
recp = ["Select recipient's address"]

def sender_mail():
    myc.execute("SELECT From_Email FROM mail_data")
    users = myc.fetchall()
    for u in users:
        for data in u:
            sender.append(str(data))

def reciever_mail():
    myc.execute("SELECT To_Email FROM to_email")
    users1 = myc.fetchall()
    for u1 in users1:
        for data1 in u1:
            if data1 != None:
                recp.append(str(data1))
            else:
                continue

def value():
    global val_r , val_s
    val_s = drop_s.get()
    val_r = drop_r.get()
    verify()

def add_s():
    global new
    var = StringVar()
    var_p = StringVar()
    new = Toplevel(root)
    new.title("Sender Details")

    label_s = tk.Label(new , text = "Mail Address : ")
    label_s.grid(row = 0 , column = 0 , pady = 10 , padx = 10 , sticky = 'E')
    add = tk.Entry(new , textvariable = var , width = 40)
    add.grid(row = 0 , column = 1 , pady = 10 , padx = 10 , sticky = 'W')
    add.focus()

    label_p = tk.Label(new , text = "Password : ")
    label_p.grid(row = 1 , column = 0 , pady = 10 , padx = 10 , sticky = 'E')
    passwd = tk.Entry(new , textvariable = var_p , width = 40)
    passwd.grid(row = 1 , column = 1 , pady = 10 , padx = 10 , sticky = 'W')

    button_user = ttk.Button(new , text = "Save" , command = lambda: insert_data(add , passwd))
    button_user.grid(row = 2 , column = 1 , pady = 5 , padx = 10 , sticky = 'W') 

def add_r():
    global new_win
    variable = StringVar()
    new_win = Toplevel(root)
    new_win.title("Recipient Details")
    frame = tk.Frame()

    label_r = tk.Label(new_win , text = "Mail Address : ")
    label_r.grid(row = 0 , column = 0 , pady = 10 , padx = 10 , sticky = 'E')
    id = tk.Entry(new_win , textvariable = variable , width = 40)
    id.grid(row = 0 , column = 1 , pady = 10 , padx = 10 , sticky = 'W')
    id.focus()

    button_user1 = ttk.Button(new_win , text = "Save" , command = lambda: insert_recipient(id))
    button_user1.grid(row = 2 , column = 1 , pady = 5 , padx = 10 , sticky = 'W') 

def verify():
    global smtp
    myc.execute("SELECT Password FROM mail_data WHERE From_Email = (%s)" , (val_s , ))
    ver_str = myc.fetchone()
    if ver_str != None:
        for v in ver_str:
            try:
                server_dict = {'gmail': 'smtp.gmail.com', 'outlook': 'smtp-mail.outlook.com', 'yahoo': 'smtp.mail.yahoo.com', 'proton': 'smtp.protonmail.ch', 'protonmail': 'smtp.protonmail.ch'}
                decide = val_s.split("@")
                server_decide = decide[1].split(".") 
                serve = server_decide[0]
                if serve in server_dict.keys():
                    server = server_dict[serve] 
                    smtp = smtplib.SMTP(server , 587)
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login(val_s , str(v))
                    label = tk.Label(root , text = "Verified !")
                    root.after(4000 , label.destroy)
                    label.grid(row = 3 , column = 1 , pady = 2 , padx = 10)
                    desc()
                else:
                    label1 = tk.Label(root , text = "Server not Supported")
                    root.after(4000 , label1.destroy)
                    label1.grid(row = 3 , column = 1 , pady = 2 , padx = 10)
            except OSError:
                label2 = tk.Label(root , text = "Error ! Please try again")
                root.after(4000 , label2.destroy)
                label2.grid(row = 3 , column = 1 , pady = 2 , padx = 10)
            except IndexError:
                label3 = tk.Label(root , text = "Error ! Please try again")
                root.after(4000 , label3.destroy)
                label3.grid(row = 3 , column = 1 , pady = 2 , padx = 10)

def insert_data(add , passwd):
    addr = add.get()
    passw = passwd.get()
    myc.execute("INSERT INTO mail_data VALUES (%s , %s)" , (addr , passw))
    mydb.commit()

    label_con1 = tk.Label(new , text = "Operation Successful")
    label_con1.grid(row = 2 , column = 1 , pady = 10 , padx = 40 , sticky = 'E')
    new.protocol("WM_DELETE_WINDOW" , lambda: refresh(new , addr , drop_s , sender))

def insert_recipient(mail_id):
    mail_add  = mail_id.get()
    myc.execute("INSERT INTO to_email VALUES (%s)" , (mail_add , ))
    mydb.commit()

    label_con = tk.Label(new_win , text = "Operation Successful")
    label_con.grid(row = 2 , column = 1 , pady = 10 , padx = 40 , sticky = 'E')
    new_win.protocol("WM_DELETE_WINDOW" , lambda: refresh(new_win , mail_add , drop_r , recp))

def refresh(win_ , data , box , list_):
    win_.destroy()
    box.configure(values = ())   
    list_.append(data)
    box["values"] = list_ 

def desc():
    global window
    window = Toplevel(root)
    window.title("Body and Attachments")
    fr = tk.Frame(window)

    sub = tk.Label(window , text = "Subject : ")
    sub.grid(row = 0 , column = 0 , pady = 10 , padx = 10 , sticky = 'W')
    sub_text = tk.Entry(window , textvariable = StringVar() , width = 56 )
    sub_text.grid(row = 0 , column = 1 , pady = 10 , padx = 10 , sticky = 'W')
    sub_text.focus()

    label_body = tk.Label(window , text = "Body : ")
    label_body.grid(row = 1 , column = 0 , pady = 10 , padx = 10 , sticky = 'E')
    text_box = scrolledtext.ScrolledText(window , width = 56 , height = 6 , font = ("Segoe UI" , 9))
    text_box.grid(row = 1 , column = 1 , pady = 10 , padx = 10 , sticky = 'W')

    global filenames 
    filenames = ()
    button_file = ttk.Button(window , text = "Add Attachments" , command = lambda: open_files())
    button_file.grid(row = 2 , column = 1 , pady = 10 , padx = 10 , sticky = 'W')

    button_send = ttk.Button(window , text = "Send Mail" , command = lambda: send_mail(sub_text , text_box))
    button_send.grid(row = 2 , column = 1 , pady = 10 , padx = 26 , sticky = 'E')

def open_files():
    global filenames
    files = list(filenames)
    filetypes = (('Text Files' , '*.txt') , ('Word Document' , '*.docx') , ('Image File (.jpg)' , '*.jpg') , ('Image File (.png)' , '*.png') , ('PDF File' , '*.pdf') , ('All Files' , '*.*'))
    files.extend(fd.askopenfilenames(title = "Add Files" , initialdir = '/' , filetypes = filetypes))
    for f in files:
        if f == '':
            files.remove(f)
    filenames = tuple(files)

    if filenames != ():
        file_label = tk.Label(window , text = "Attachments Added")
        file_label.grid(row = 2 , column = 1 , pady = 10 , padx = 10)
        window.after(2800 , file_label.destroy)

def send_mail(subject , body_email):
    try:
        global smtp
        msg = MIMEMultipart()
        msg["From"] = val_s
        msg["To"] = val_r
        msg["Subject"] = subject.get()
        message = body_email.get("1.0" , tk.END)
        msg.attach(MIMEText(message , "plain"))
        if filenames != ():
            for file in filenames:
                file_ = open(file , "rb")
                add_file = MIMEBase("application" , "octet-stream")
                add_file.set_payload(file_.read())
                encoders.encode_base64(add_file)
                splited = file.split('/')
                file_name = splited[-1] 
                add_file.add_header("content-disposition" , "attachment" , filename = file_name)
                msg.attach(add_file)
            text_ = msg.as_string()
        else:
            text_ = msg.as_string()
        smtp.sendmail(val_s , val_r , text_)
        file_send = tk.Label(window , text = "Sent Successfully")
        file_send.grid(row = 2 , column = 1 , pady = 10 , padx = 10)
        window.after(4000 , file_send.destroy)
    except OSError:
        label4 = tk.Label(window , text = "Error ! Please try again")
        label4.grid(row = 2 , column = 1 , pady = 10 , padx = 10)

def main_loop():
    root.title("Mail Client")

    sender_mail()
    lab_s = tk.Label(root , text = "From : ")
    lab_s.grid(row = 0 , column = 0 , pady = 10 , padx = 10 , sticky = 'E')
    clicked_s = tk.StringVar()
    global drop_s
    drop_s = ttk.Combobox(root , width = 40 , textvariable = clicked_s , state = "readonly")
    drop_s["values"] = sender
    drop_s.bind("<<ComboboxSelected>>" , lambda e : root.focus())
    drop_s.current(0)
    drop_s.grid(row = 0 , column = 1 , pady = 10 , padx = 10 , sticky = 'W') 

    reciever_mail()
    lab_r = tk.Label(root , text = "To : ")
    lab_r.grid(row = 1 , column = 0 , pady = 10 , padx = 10 , sticky = 'E')
    clicked_r = tk.StringVar()
    global drop_r
    drop_r = ttk.Combobox(root , width = 40 , textvariable = clicked_r , state = "readonly")
    drop_r["values"] = recp
    drop_r.bind("<<ComboboxSelected>>" , lambda p : root.focus())
    drop_r.current(0)
    drop_r.grid(row = 1 , column = 1 , pady = 5 , padx = 10 , sticky = 'W') 

    button_s = ttk.Button(root , text = "Add Sender" , command = add_s)
    button_s.grid(row = 0 , column = 2 , pady = 5 , padx = 10) 

    button_r = ttk.Button(root , text = "Add Recipient" , command = add_r)
    button_r.grid(row = 1 , column = 2 , pady = 5 , padx = 10 , sticky = 'W') 

    button_ver =  ttk.Button(root , text = "Verify Details" , command = value)
    button_ver.grid(row = 2 , column = 1 , pady = 5 , padx = 10)

    root.mainloop()


user = input("Enter MySQL Username : ")
password_ = input("Enter MySQL Password : ")
status = create_database(user , password_)

root = tk.Tk()

if status == 0 or status == 1007:
    mydb = mysql.connector.connect(host = "localhost" , user = user , passwd = password_ , database = "Mail")
    myc = mydb.cursor()
    icon = tk.PhotoImage(file = "C:\\Users\\Bhavya Jain\\Downloads\\Mail_Client.png")
    root.iconphoto(True , icon)
    main_loop()
else:
    print(status)