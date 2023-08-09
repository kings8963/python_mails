from tkinter import *
import mysql.connector

#Connection to the db
def connection(query, value):
    mydb = mysql.connector.connect(
    host="192.168.0.161",
    user="db",
    password="OthelO@492",
    database="cumple"
    )
    #Show
    if query == 's':
        mycursor = mydb.cursor()
        mycursor.execute(""" SELECT * FROM Persons """)
        myresult = mycursor.fetchall()
        mycursor.close()
        return myresult

    #Delete
    if query == 'd':
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT id FROM Persons WHERE id='{value}'")
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
           mycursor.execute(f" DELETE FROM Persons WHERE id='{value}'")
           mydb.commit()
           return True
        else:
            return False
    
    #Add
    if query == 'a':
        mycursor = mydb.cursor()
        mycursor.execute(f"INSERT INTO Persons VALUES('{value[0]}', '{value[1]}', '{value[2]}', '{value[3]}')")
        mydb.commit()
        return True

#Window of "show" function when "Agregar empleado" button is pressed
def show():
    result = connection('s',0)
    newWindow = Toplevel()
    newWindow.title("Mostrar")
    newWindow.geometry("500x400")
    newWindow.resizable(0,0)
    scrollbar = Scrollbar(newWindow, orient="vertical")
    lb = Listbox(newWindow, width=50, height=20, yscrollcommand=scrollbar.set)
    scrollbar.config(command=lb.yview)
    scrollbar.pack(side="right", fill="y")
    lb.pack(side="left",fill="both", expand=True)
    for values in result:
        if '{' in values:
            values.replace("{'",'')
            values.replace("}'",'')
        lb.insert(END, values)
        lb.insert(END,'\n')

#window error when an error happens
def error(flag):
    text_m = ""

    newWindow = Toplevel()
    newWindow.title("ERROR")
    newWindow.geometry("500x100")
    newWindow.resizable(0,0)

    #Type of errors
    if flag == 1:
        text_m = "Error al ingresar los datos"
    elif flag == 2:
        text_m = "El usuario no existe"
        

    widget3 = Button(newWindow, text='Aceptar', command=newWindow.destroy, padx=10, pady=10, width = 15)
    widget3.place(x=170,y=50)

    label = Label(newWindow, text=text_m, padx=20, pady=15)
    label.pack()

#Window to show succesful changes
def accept():
    newWindow = Toplevel()
    newWindow.title("ERROR")
    newWindow.geometry("500x100")
    newWindow.resizable(0,0)

    widget3 = Button(newWindow, text='Aceptar', command=newWindow.destroy, padx=10, pady=10, width = 15)
    widget3.place(x=170,y=50)

    label = Label(newWindow, text='Movimiento exitoso', padx=20, pady=15)
    label.pack()

# Function to delete when "Eliminar empleado" button is pressed
def delete():
    newWindow = Toplevel()
    newWindow.title("Eliminar")
    newWindow.geometry("500x200")
    newWindow.resizable(0,0)

    label = Label(newWindow, text="Ingrese el número de empleado:", padx=20, pady=15)
    label.pack()

    entry = Entry(newWindow, justify=CENTER, width=20 )
    entry.place(x=180, y=50)

    def get():
        guess = entry.get()
        try:
            int(guess) #If the user type a numer the program will contine, then will show the error window
            if connection('d', guess):
                accept()
            else:
                error(2)
        except:
            error(1)
        

    widget3 = Button(newWindow, text='Eliminar', command=get, padx=10, pady=10, width = 15)
    widget3.place(x=170,y=100)


#Function to verify the input birthday 
def data_verification(values):
    date = values[2].split('-')
    try:
        if int(date[0]) > 1900:
            if int(date[1]) > 0 and int(date[1]) <= 12:
                if int(date[2]) >= 1 and int(date[2]) <= 31:
                    return True
    except:
            return False
     

#Function to add when "Agregar empleado" is pressed
def insert():
    newWindow = Toplevel()
    newWindow.title("Agregar")
    newWindow.geometry("500x350")
    newWindow.resizable(0,0)

    label = Label(newWindow, text="Ingrese el número de empleado:", padx=20, pady=15)
    label.pack()

    label_name = Label(newWindow, text="Nombre:")
    label_name.place(x=40, y=70)
    name = Entry(newWindow, justify=CENTER, width=20 )
    name.place(x=40, y=90)

    label_lastname = Label(newWindow, text="Apellido:")
    label_lastname.place(x=190, y=70)
    last_name = Entry(newWindow, justify=CENTER, width=20 )
    last_name.place(x=190, y=90)

    label_birth = Label(newWindow, text="Fecha: (AAAA-MM-DD)")
    label_birth.place(x=340, y=70)
    birth = Entry(newWindow, justify=CENTER, width=20 )
    birth.place(x=340, y=90)

    label_ide = Label(newWindow, text="Número de empleado:")
    label_ide.place(x=40, y=180)
    ide = Entry(newWindow, justify=CENTER, width=20 )
    ide.place(x=40, y=200)

    def get():
        #Adds all the inputs into a list
        data = []
        data.append(name.get())
        data.append(last_name.get())
        data.append(birth.get())
        data.append(ide.get())
        
        try:
            int(data[3])    #If the number of slave is a number and not a string, the program will continue, the will show the error window
            if data_verification(data):
                if connection("a", data):
                    accept()
            else:
                error(1)
        except:
            error(1)

    widget3 = Button(newWindow, text='Agregar', command=get, padx=10, pady=10, width = 15)
    widget3.place(x=170,y=250)

def update():
    print("Hola mundo")


root = Tk(className='Modificador de registros')
root.resizable(0,0)
root.geometry("500x550")

label = Label(root, text="Base de datos de cumpleaños", padx=10, pady=10)
label.pack()
widget = Button(root, text='Mostrar registros', command=show, padx=10, pady=10, width = 15)
widget.place(x=180,y=100)

widget2 = Button(root, text='Eliminar empleado', command=delete, padx=10, pady=10, width = 15)
widget2.place(x=180,y=200)

widget3 = Button(root, text='Agregar empleado', command=insert, padx=10, pady=10, width = 15)
widget3.place(x=180,y=300)

widget4 = Button(root, text='Actualizar datos', command=update, padx=10, pady=10, width = 15)
widget4.place(x=180,y=400)




root.mainloop()
