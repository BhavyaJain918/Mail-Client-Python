import mysql.connector
def create_database(username , password):
    try:
        mydb = mysql.connector.connect(host = "localhost" , user = username, passwd = password)
        mycursor = mydb.cursor()
        try:
            mycursor.execute("CREATE DATABASE Mail")
            mycursor.execute("USE Mail")
            mycursor.execute("CREATE TABLE Mail_Data (From_Email varchar(40) NOT NULL PRIMARY KEY , Password varchar(20) NOT NULL)")
            mydb.commit()
            mycursor.execute("CREATE TABLE To_Email (To_Email varchar(40) NOT NULL)")
            mydb.commit()
            mycursor.close()
            mydb.close()
            return 0
        except mysql.connector.errors.DatabaseError as d:
            mycursor.close()
            mydb.close()
            return d.errno
    except mysql.connector.errors.ProgrammingError as e:
        return (f"Error occurred: {e}")
    
if __name__ == "__main__":
    username = input("Enter username: ")
    password = input("Enter password: ")
    create_database(username , password)