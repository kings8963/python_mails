
'''

Herramienta automatizada para mandar correos de cumpleaños

'''
from email.mime.text import MIMEText
from smtplib import SMTP
from datetime import date
import mysql.connector

def connection_db(date):
    #Create connection with the DB credentials.
    mydb = mysql.connector.connect(
    host="localhost",
    user="eguzman",
    password="OthelO@492",
    database="empleados2"
    )
    mycursor = mydb.cursor()
    #Query in the DB.
    #Get brithdays of all the slaves from today's date.
    mycursor.execute("SELECT name, last_name, birth FROM Persons WHERE extract(DAY FROM birth) = %s and extract(MONTH FROM birth) = %s"%(date[2],date[1]))
    myresult = mycursor.fetchall()
    mycursor.close()
    #If no one have a birthday in today's date, program stops.
    if len(myresult) < 1:
        return False
    write_message(myresult) #If not, write message


def write_message(users):
    full_names = [] #List of names
    string = "" #Names separated by ","
    if len(users) > 1: #If two or more names
        for i in range(len(users)):
            full_names.append(users[i][0] + ' ' + users[i][1])
            if i == 0:
                string = str(full_names[i].split("'")) + ', '
            elif (i+1) == len(users):
                string += str(full_names[i].split("'"))
            else:
                string += str(full_names[i].split("'")) + ', '
        string = string.replace("['",'')
        string = string.replace("']",'')
        text = f"Estimados {string}, Pertek-Erler les manda un gran abrazo y los felicita en este día especial."
    else: #If one name
        string = users[0][0] + ' ' + users[0][1]
        string = string.replace("['",'')
        string = string.replace("']",'')
        text = f"Estimad@ {string}, Pertek-Erler les manda un gran abrazo y los felicita en este día especial."
    send_email(text)
         
def send_email(message):
    try:
        sender = "eguzman@pertek-erler.com"
        to = "eguzman@pertek-erler.com"
        server = 'smtp.gmail.com:587'
        msg = MIMEText(message.encode('utf-8'), _charset='utf-8')
        msg['Subject'] = 'Feliz Cumpleaños'
        msg['From'] = sender
        msg['To'] = to
        password = 'gakbmlkuacoaqsgh'
        s = SMTP(server)
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, [to], msg.as_string())
        s.quit()
    except:
        print("error")


#main
if __name__ == "__main__":
    current_date = str(date.today()) #Get today's date
    date_values = current_date.split('-') #Separate year,month,day. Save them into a new list
    connection_db(date_values)  #Call the connection to the DB.