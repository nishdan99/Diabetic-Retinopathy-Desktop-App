from tkinter import *
# loading Python Imaging Library
from PIL import ImageTk, Image
# To get the dialog box to open when required
from tkinter import filedialog
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model, load_model
import sqlite3
import numpy as np
from tkinter import messagebox
import os.path
from os import path
import sys
import os
from datetime import date



file_exist = path.exists("test.db")
if file_exist==False:
    #create database
    conn = sqlite3.connect('test.db')
    #create cursor
    c = conn.cursor()
    #create table
    c.execute("""
            CREATE TABLE test (
            firstName text,
            lastname text,
            email text,
            Phone text,
            Address text,
            Age text,
			Result text,
            date text
            )
    """)
    conn.commit()
    conn.close()
else:
    pass


model = load_model('weights.hdf5')
#model.compile(loss='binary_crossentropy',

              #optimizer='rmsprop',

              #metrics=['accuracy'])
def open_img():
	# Select the Imagename from a folder
	global x
	x = openfilename()

	# opens the image
	img = Image.open(x)

	# resize the image and apply a high-quality down sampling filter
	img = img.resize((250, 250), Image.ANTIALIAS)

	# PhotoImage class is used to add image to widgets, icons etc
	img = ImageTk.PhotoImage(img)

	# create a label
	panel = Label(root, image = img)

	# set the image as img
	panel.image = img
	panel.place(x = 350 ,y =100)

def openfilename():

	# open file dialog box to select image
	# The dialogue box has a title "Open"
	filename = filedialog.askopenfilename(title ='"pen')
	return filename

def submit():
    global Result
    Result = 100
    img= Image.open(x)
	# resizing the image to (256,256)
    img = img.resize((256,256))
	# converting image to array
    img = np.asarray(img, dtype= np.float32)
	# normalizing the image
    img = img / 255
	# reshaping the image in to a 4D array
    img = img.reshape(-1,256,256,3)
	# making prediction of the model
    predict = model.predict(img)
	# getting the index corresponding to the highest value in the prediction
    predict = np.argmax(predict)
    classess = ['Mild', 'Moderate', 'No Diabetic Retinopathy', 'Proliferate Diabetic Retinopathy', 'Severe']
    Result = classess[predict]
    if predict == 2:
    	text_result = "Patient is safe No diabetic Retinopathy detected"
    else:
	    text_result = "Patient has diabetic Retinopathy, and stage is " + Result
    my_label = Label(root, text = text_result, bg = '#edc7b7' , fg = '#123c69')
    my_label.place(x = 350 ,y =450)

Result = ""

def checkDetails(): #To check whether details entered are valid
    if firstName.get() == "":
        msg_to_user = "First Name Feild is Empty!!!"
        return messagebox.showwarning ('warning',msg_to_user)

    elif lastName.get() == "":
        msg_to_user = "Last Name Feild is Empty!!!"
        return messagebox.showwarning ('warning',msg_to_user)

    elif email.get() == "":
        msg_to_user = "Please fill the email id"
        return messagebox.showwarning ('warning',msg_to_user)

    elif Phone.get() == "":
        msg_to_user = "Phone number not found"
        return messagebox.showwarning ('warning',msg_to_user)

    elif Address.get() == 0 :
        msg_to_user = "Address Field is Empty!!"
        return messagebox.showwarning ('warning',msg_to_user)

    elif Age.get() =='':
        msg_to_user = "Age feild required!!!"
        return messagebox.showwarning ('warning',msg_to_user)
    elif email.get() ==0:
        msg_to_user = "Email feild required!!!"
        return messagebox.showwarning ('warning',msg_to_user)
    elif var1.get() == 0 or var2.get() == 0:
        msg_to_user = "Accept terms and conditions"
        return messagebox.showwarning ('warning',msg_to_user)
    else:
        submit()

def saveDetails(): #To check whether details entered are valid
    if firstName.get() == "":
        msg_to_user = "First Name Feild is Empty!!!"
        return messagebox.showwarning ('warning',msg_to_user)

    elif lastName.get() == "":
        msg_to_user = "Last Name Feild is Empty!!!"
        return messagebox.showwarning ('warning',msg_to_user)

    elif email.get() == "":
        msg_to_user = "Please fill the email id"
        return messagebox.showwarning ('warning',msg_to_user)

    elif Phone.get() == "":
        msg_to_user = "Phone number not found"
        return messagebox.showwarning ('warning',msg_to_user)

    elif Address.get() == 0 :
        msg_to_user = "Address Field is Empty!!"
        return messagebox.showwarning ('warning',msg_to_user)

    elif Age.get() =='':
        msg_to_user = "Age feild required!!!"
        return messagebox.showwarning ('warning',msg_to_user)
    elif email.get() ==0:
        msg_to_user = "Email feild required!!!"
        return messagebox.showwarning ('warning',msg_to_user)
    elif Result == "":
        msg_to_user = "click on test first!!!"
        return messagebox.showwarning ('warning',msg_to_user)
    else:
        Savetodb()


def Savetodb():
    today = date.today()

    # dd/mm/YY
    d1 = today.strftime("%d/%m/%Y")
    print("d1 =", d1)
    #create database
    conn = sqlite3.connect('test.db')
    #create cursor
    c = conn.cursor()
    #create table
    #insert value
    c.execute("INSERT INTO test VALUES(:fname, :lname, :email, :Phone, :Address, :Age, :Result, :date)",{
            'fname': entry_firstName.get(),
            'lname': entry_lastName.get(),
            'email': entry_email.get(),
            'Phone': entry_phone.get(),
            'Address': entry_address.get("1.0",'end-1c'),
            'Age': entry_age.get(),
			'Result': Result,
            'date': d1
    })
    x = entry_firstName.get()
    c.execute("SELECT * FROM test")
    record = c.fetchall()
    print(record)
    conn.commit()
    conn.close()

def resetDetails():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

def searchDetails():
    #create database
    conn = sqlite3.connect('test.db')
    #create cursor
    c = conn.cursor()
    x = firstNamesearch.get()
    y = phonesearch.get()
    c.execute("SELECT * FROM test WHERE firstName = ? AND ?;",[x, y])
    record = c.fetchall()
    final = record[-1][0] + ' ' + record[-1][1] + ' previously checked on '+ record[-1][7] + ' and result was ' + record[-1][6]
    searchresult.set(final)
    conn.commit()
    conn.close()

def LoadDetails():
    #create database
    conn = sqlite3.connect('test.db')
    #create cursor
    c = conn.cursor()
    x = firstNamesearch.get()
    y = phonesearch.get()
    c.execute("SELECT * FROM test WHERE firstName = ? AND ?;",[x, y])
    record = c.fetchall()
    firstName.set(record[-1][0])
    lastName.set(record[-1][1])
    email.set(record[-1][2])
    Phone.set(record[-1][3])
    Age.set(record[-1][5])
    conn.commit()
    conn.close()



# for the app interface
root = Tk()
root.title("Diabetic Retinopathy Detection")
title  =Label(root,text ="Pre Detection Of Diabetes Rethinopathy",bg="#edc7b7",width ="300",height="2",fg ="#123c69",font=("Calibri 20 bold italic underline")).pack()
root['background']='#eee2dc'
root.geometry("800x500")
myCanvas = Canvas(root, bg="white", height=1, width=850).place(x=0, y= 500)
myCanvas1 = Canvas(root, bg="white", height=800, width=1).place(x=850, y= 72)

firstName = Label(root,text = "First Name: ",fg = "#ac3b61", bg ='#eee2dc' ,font = ("Verdana 12")).place(x= 12 , y=100)
lastName = Label(root,text = "Last Name: ",fg = "#ac3b61", bg ='#eee2dc',font = ("Verdana 12")).place(x= 12 , y=140)
email =Label(root,text = "Email: ",fg = "#ac3b61", bg ='#eee2dc',font = ("Verdana 12")).place(x= 12 , y=180)
Phone = Label(root,text = "Phone: ",fg = "#ac3b61", bg ='#eee2dc',font = ("Verdana 12")).place(x= 12 , y=220)
Address = Label(root,text = "Address: ",fg = "#ac3b61", bg ='#eee2dc',font = ("Verdana 12")).place(x= 12 , y=260)
Age = Label(root,text = "Age: ",fg = "#ac3b61", bg ='#eee2dc',font = ("Verdana 12")).place(x= 12 , y=320)

Gender = Label(root,text = "Gender: ",fg = "#ac3b61", bg ='#eee2dc',font = ("Verdana 12")).place(x= 12 , y=360)
radio = StringVar()
Male = Radiobutton(root,text = "Male",fg = "#ac3b61", bg ='#eee2dc',variable =radio,value = "Male",font = ("Verdana 12")).place(x=12, y=400)
Female = Radiobutton(root,text = "Female",fg = "#ac3b61", bg ='#eee2dc',variable =radio,value = "Female",font = ("Verdana 12")).place(x=120, y=400)

firstName = StringVar()
lastName = StringVar()
email = StringVar()
Phone = StringVar()
Address = StringVar()
Age = StringVar()
Gender = StringVar()


entry_firstName = Entry(root,textvariable = firstName,width = 30, bg = '#edc7b7' , fg = '#123c69')
entry_firstName.place(x=120, y= 100)

entry_lastName = Entry(root,textvariable = lastName,width = 30, bg = '#edc7b7' , fg = '#123c69')
entry_lastName.place(x=120, y= 140)

entry_email = Entry(root,textvariable = email,width = 30, bg = '#edc7b7' , fg = '#123c69')
entry_email.place(x=120, y= 180)

entry_phone = Entry(root,textvariable = Phone,width = 30, bg = '#edc7b7' , fg = '#123c69')
entry_phone.place(x=120, y= 220)

entry_address =Text(root,height = 2, width = 23, bg = '#edc7b7' , fg = '#123c69')
entry_address.place(x= 119,y=260)
# entry_address.pack(pady =20)

entry_age = Entry(root,textvariable = Age, width = 30, bg = '#edc7b7' , fg = '#123c69')
entry_age.place(x=120,y=320)

UploadButton = Button(root,text="Upload Image",width = 12,height = 1,bg= "#bab2b5", fg = '#ac3b61',font=("Calibri 12"),command = open_img).place(x = 350 ,y =400)
TestButton = Button(root,text ="Test", width = 12,height=1,bg = "#bab2b5", fg = '#ac3b61',font=("Calibri 12") , command  =checkDetails).place(x=500,y=400)
SaveButton = Button(root,text ="Save", width = 12,height=1,bg = "#bab2b5", fg = '#ac3b61',font=("Calibri 12") , command  =saveDetails).place(x=12,y=450)
ResetButton = Button(root,text ="Reset", width = 12,height=1,bg = "#bab2b5", fg = '#ac3b61',font=("Calibri 12") , command  =resetDetails).place(x=162,y=450)


canvas = Canvas(root, width = 500, height = 750)
canvas.place(x=950, y=85)
img = PhotoImage(file="termsnservice.png")
canvas.create_image(1,1,anchor=NW, image=img)

var1 = IntVar()
checkbox1 = Checkbutton(root, variable=var1).place(x=1020, y= 615)
var2 = IntVar()
checkbox1 = Checkbutton(root, variable=var2).place(x=1020, y= 670)

firstNamesearch = Label(root,text = "First Name: ",fg = "#ac3b61", bg ='#eee2dc' ,font = ("Verdana 12")).place(x= 12 , y=550)
firstNamesearch = StringVar()
entry_firstNamesearch = Entry(root,textvariable = firstNamesearch,width = 30, bg = '#edc7b7' , fg = '#123c69').place(x=180, y=550)

Phonesearch = Label(root,text = "Phone: ",fg = "#ac3b61", bg ='#eee2dc' ,font = ("Verdana 12")).place(x= 12 , y=590)
phonesearch = StringVar()
entry_phoneNamesearch = Entry(root,textvariable = phonesearch,width = 30, bg = '#edc7b7' , fg = '#123c69').place(x=180, y=590)

SearchButton = Button(root,text ="Search", width = 12,height=1,bg = "#bab2b5", fg = '#ac3b61',font=("Calibri 12") , command  =searchDetails).place(x=32,y=640)
LoadButton = Button(root,text ="Load", width = 12,height=1,bg = "#bab2b5", fg = '#ac3b61',font=("Calibri 12") , command  =LoadDetails).place(x=182,y=640)

searchresult = StringVar()
search_result = Entry(root,textvariable = searchresult,width = 100, bg = '#edc7b7' , fg = '#123c69').place(x=12, y=700)



# for continues loop
root.mainloop()
