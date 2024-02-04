import mysql.connector
import sys
from Init_SQL import create_database
from Mail_Client import email_func
def insert_data():
    if status == 0 or status == 1007: 
        try:
            password_my = ""
            email = input("Enter sender's email address: ")
            myc.execute("SELECT Password FROM User WHERE Email = (%s)" , (email , ))
            password_user = myc.fetchone()
            if password_user == None:
                password_inp = input("Enter password: ")
                myc.execute("INSERT INTO User VALUES (%s , %s)" , (email , password_inp))
                mydb1.commit()
                print("Password saved in database.Logging in...")
                email_func(email , password_inp)
            else:
                for data in password_user:
                    password_my += str(data)
                print("Password found in database.Logging in...")
                email_func(email , password_my)
        except mysql.connector.errors.DataError as de:
            print(f"Error occurred: {de}")
    else:
        print(status)

def update_data():
    if status == 1007:
        try:
            myc.execute("SELECT Email FROM User")
            email_id = myc.fetchone()
            if email_id != None:
                set_email = input("Enter email address: ")
                for e in email_id:
                    if set_email == str(e):
                        new_passwd = input("Enter new password: ")
                        myc.execute("UPDATE User SET Password = (%s) WHERE Email = (%s)" , (new_passwd , set_email))
                        mydb1.commit()
                        print("Password updated")
                    else:
                        print(f"Address {set_email} not present in database")
            else:
                print("No records found in database")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Error occurred: {e}")
        except mysql.connector.errors.DatabaseError as d:
            print(f"Error occurred: {d}")
    else:
        print(status)
        
def delete_data():
    myc.execute("SELECT 1 FROM User LIMIT 1")
    cnt = myc.fetchone()
    if cnt != None:
        delete = input("Enter email address to be deleted: ")
        myc.execute("SELECT COUNT(Email) FROM User WHERE Email = (%s)" , (delete , ))
        obj = myc.fetchone()
        if obj != (0 , ):
            myc.execute("DELETE FROM User WHERE Email = (%s)" , (delete , ))
            mydb1.commit()
            print("Data deleted successfully")
        else:
            print("Data not found")
    else:
        print(f"No record found in database")


user = input("Enter username: ")
passw = input("Enter password: ")
status = create_database(user , passw)
try:
    mydb1 = mysql.connector.connect(host = "localhost" , user = user, passwd = passw , database = "Mail")
    myc = mydb1.cursor(buffered = True)
except mysql.connector.errors.ProgrammingError as e:
        print(f"Error occurred: {e}")
        sys.exit()
print("Press\n1. To send mails\n2. To update password\n3. To delete a mail address\n0. To exit")
while True:
    ch = int(input("Enter your choice: "))
    match(ch):
        case 1:
            insert_data()
        case 2:
            update_data()
        case 3:
            delete_data()
        case 0:
            break
        case _:
            print("Enter correct values")
myc.close()
mydb1.close()