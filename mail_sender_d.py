#!/usr/bin/python
'''

Herramienta automatizada para mandar correos de cumpleaños

'''

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from datetime import date
import mysql.connector
import os

def connection_db(date):
    #Create connection with the DB credentials.
    mydb = mysql.connector.connect(
    host="192.168.0.161",
    user="db",
    password="OthelO@492",
    database="cumple"
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
    if len(users) > 1: #If two or more names
        for i in range(len(users)):
            text = f"{users[i][0] + ' ' + users[i][1]}"
            print(text)
            send_email(text)
    else: #If one name
        text = f"{users[0][0] + ' ' + users[0][1]}"
        send_email(text)

def send_email(message):
    url = 'https://e00-marca.uecdn.es/assets/multimedia/imagenes/2022/07/14/16578308727069.jpg'

    try:
        sender =  "eguzman@pertek-erler.com" #"auxrh@pertek-erler.com"
        to = "eguzman@pertek-erler.com" #"pertek_erler_all_employees@pertek-erler.com"
        server = 'smtp.gmail.com:587'
        msg = MIMEMultipart()
        text = MIMEText('<html><body><h1>¡¡Feliz Cumpleaños!!</h1>' + '<p>De parte del equipo de <b>Pertek-Erler</b> ¡¡MUCHAS FELICIDADES!!</p>'+ f'<b>{message}</b>, esperamos que tengas un excelente día.  :)' + f'<p><img src="{url}" width="80%"></p>' + '</body></html>', 'html', 'utf-8')
        msg.attach(text)
        msg['Subject'] = f'¡¡Feliz Cumpleaños {message}!!'
        msg['From'] = sender
        msg['To'] = to
        password =  'gakbmlkuacoaqsgh' #'RAMOS1997' 
        s = SMTP(server)
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, [to], msg.as_string())
        s.quit()
        print("done :)")

    except:
        print("error")

#main
if __name__ == "__main__":
    current_date = str(date.today()) #Get today's date
    date_values = current_date.split('-') #Separate year,month,day. Save them into a new list
    connection_db(date_values)  #Call the connection to the DB.