import binascii
import itertools
import random
import string
import hashlib
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sqlite3

conn = sqlite3.connect('e_voting_user_data.db')
c = conn.cursor()

def enter():
    a = (e1.get())
    password = (e2.get())
    unique = True

    for value in c.execute('SELECT username FROM users'):
        username = value[0]
        if username == a:
            print('Username already exists')
            tk.Label(adminWindow,text='Username already exists',foreground='red').grid(row=6,column=0,padx=10,sticky=tk.W)
            unique = False
            break

    if unique == True:
        letters = string.ascii_letters
        h = hashlib.md5(password.encode())
        passwordHash = h.hexdigest()
        c.execute("INSERT INTO users (userName, password) VALUES (?, ?)",
        (a, passwordHash))
        conn.commit()
        tk.Label(adminWindow,text='Voter added successfuly',foreground='green').grid(row=6,column=0,padx=10,sticky=tk.W)

    for row in c.execute('SELECT * FROM users'):
        print(row)

def change():
    password = (e5.get(),)
    print (password)
    c.execute("UPDATE admin SET password =? WHERE userName = 'Admin'", (password))
    conn.commit()
    tk.Label(changePasswordWindow, text='Password updated',foreground='green').grid(row=5,column=0,padx=10,sticky=tk.W)
    print('Password updated')

def return_screen():
    changePasswordWindow.withdraw()
    adminWindow.deiconify()
    

def changePassword():
    adminWindow.withdraw()
    global changePasswordWindow
    changePasswordWindow = tk.Tk()
    changePasswordWindow.title('')
    changePasswordWindow.geometry('360x140')
    
    tk.Label(changePasswordWindow,foreground='black',font=1,height=1,padx=8,pady=15, 
         text="Password").grid(row=0,sticky=tk.W)
    
    global e5
    
    e5 = tk.Entry(changePasswordWindow,fg='black',bg='yellow',width=20,font=1)
    e5.grid(row=0, column=1)
    
    tk.Button(changePasswordWindow, 
          text='Update',font=1,width=8,bg='red',fg='yellow', 
          activebackground = "red",command=change).grid(row=4, 
                                    column=0, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(changePasswordWindow, 
          text='Return',font=1,width=8,bg='red',fg='yellow', 
          activebackground = "red",command=return_screen).grid(row=4, 
                                    column=1, 
                                    sticky=tk.E,
                                    padx=0,
                                    pady=5)
    

def tally():
    Bob = 0
    Alice = 0
    Eve = 0
    Sam = 0

    for value in c.execute('SELECT vote FROM votes'):
        choice = value[0]
        if choice == 'Bob':
            Bob += 1
        elif choice == 'Alice':
            Alice += 1
        elif choice == 'Eve':
            Eve += 1
        elif choice == 'Sam':
            Sam += 1
        print(value)
    print ('Bob: ' + str(Bob))
    print ('Alice: ' + str(Alice))
    print ('Eve: ' + str(Eve))
    print ('Sam: ' + str(Sam))

    tk.Label(adminWindow, text='----------------------------------').grid(row=6,column=1,padx=0,sticky=tk.W)
    tk.Label(adminWindow, text='Tally Results').grid(row=7,column=1,padx=0,sticky=tk.W)
    tk.Label(adminWindow, text='----------------------------------').grid(row=8,column=1,padx=0,sticky=tk.W)
    tk.Label(adminWindow, text='Bob: ' + str(Bob)).grid(row=9,column=1,padx=0,sticky=tk.W)
    tk.Label(adminWindow, text='Alice: ' + str(Alice)).grid(row=10,column=1,padx=0,sticky=tk.W)
    tk.Label(adminWindow, text='Eve: ' + str(Eve)).grid(row=11,column=1,padx=0,sticky=tk.W)
    tk.Label(adminWindow, text='Sam: ' + str(Sam)).grid(row=12,column=1,padx=0,sticky=tk.W)
    
def home():
    master.deiconify()
    adminWindow.withdraw()
    e3.delete(0, 'end')
    e4.delete(0, 'end')
    


def admin():
    global adminWindow
    adminWindow = tk.Tk()
    adminWindow.title('e-voting admin')
    adminWindow.geometry('425x380')
    
    tk.Label(adminWindow,foreground='black',font=1,height=1,padx=8,pady=15, 
         text="Username").grid(row=0,sticky=tk.W)
    tk.Label(adminWindow,foreground='black',font=1,height=1,padx=8,pady=10,anchor='w', 
         text="Password").grid(row=1,sticky=tk.W)

    global e1
    global e2

    e1 = tk.Entry(adminWindow,fg='black',bg='yellow',width=20,font=1)
    e2 = tk.Entry(adminWindow,fg='black',bg='yellow',width=20,font=1)


    e1.grid(row=0,column=0,columnspan=2,padx=110,sticky=tk.E)
    e2.grid(row=1,column=0,columnspan=2,padx=110,sticky=tk.E)


    tk.Button(adminWindow, 
          text='Register Voter',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=enter).grid(row=4, 
                                    column=0, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(adminWindow, 
          text='Change password',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=changePassword).grid(row=4, 
                                    column=1, 
                                    sticky=tk.W,
                                    padx=0,
                                    pady=5)

    tk.Button(adminWindow, 
          text='Tally Votes',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=tally).grid(row=5, 
                                    column=0, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(adminWindow, 
          text='Home',font=1,width=15,bg='red',fg='yellow', 
          activebackground = "red",command=home).grid(row=5, 
                                    column=1, 
                                    sticky=tk.W,
                                    padx=0,
                                    pady=5)

    

def vote():
    vote = (options1.get())
    print(username)
    print (vote)
    Bob = 0
    Alice = 0
    Eve = 0
    Sam = 0

    eligible = True

    for value in c.execute('SELECT username FROM votes'):
        eligibleUsername = value[0]
        if username == eligibleUsername:
            print('You have already voted')
            tk.Label(window,text='You have already voted.',foreground='red').grid(row=8,column=0,padx=10,sticky=tk.W)
            eligible = False
            break
    
    if eligible == True:
        c.execute("INSERT INTO votes (userName, vote) VALUES (?, ?)",
        (username, vote))
        conn.commit()
        print('Vote lodged')
        tk.Label(window,text='Vote successful',foreground='green').grid(row=8,column=0,padx=10,sticky=tk.W)
    for value in c.execute('SELECT vote FROM votes'):
        choice = value[0]
        if choice == 'Bob':
            Bob += 1
        elif choice == 'Alice':
            Alice += 1
        elif choice == 'Eve':
            Eve += 1
        elif choice == 'Sam':
            Sam += 1
        print(value)
    print ('Bob: ' + str(Bob))
    print ('Alice: ' + str(Alice))
    print ('Eve: ' + str(Eve))
    print ('Sam: ' + str(Sam))

def exitScreen():
    master.deiconify()
    window.withdraw()
    e3.delete(0, 'end')
    e4.delete(0, 'end')
    

def instructions():
    global window
    window = tk.Tk()
    window.title('e-voting terminal')
    window.geometry('360x140')
    tk.Label(window,foreground='black',font=1,height=1,padx=8,pady=15, 
         text="Select a candidate").grid(row=0,sticky=tk.W)

    global options1
    options1 = tk.StringVar(window)
    options1.set('Select') # default value
    om1 =tk.OptionMenu(window,options1, 'Bob','Alice','Eve','Sam')
    om1.grid(row=1,column=0,padx=10,sticky=tk.W)

    tk.Button(window, 
          text='Vote',font=1,width=5,bg='red',fg='yellow', 
          activebackground = "red",command=vote).grid(row=1, 
                                    column=1, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

    tk.Button(window, 
          text='Exit',font=1,width=5,bg='red',fg='yellow', 
          activebackground = "red",command=exitScreen).grid(row=1, 
                                    column=2, 
                                    sticky=tk.W,
                                    padx=15,
                                    pady=5)

def login():
    master.withdraw()
    global username
    username = (e3.get())
    password = (e4.get())

    if username == 'Admin':
        for value in c.execute('SELECT password FROM admin'):
            adminPassword = value[0]
            if adminPassword == password:
                print ('yesy')
                admin()
        
    for value in c.execute('SELECT username FROM users'):
        storedUsername = value[0]
        #print (username)
        #print (storedUsername)
        if username == storedUsername:
            print ('Name found')
            found = True
            break
        else:
            print('Name not found')
            found = False

    if found == True:
        username1 = (str(username),)
        for value in c.execute('SELECT password FROM users WHERE userName=?', username1):
            pass1 = value[0]
        print(pass1)
        print(password)
        h = hashlib.md5(password.encode())
        passwordHash = h.hexdigest()
        print(passwordHash)
        if pass1 == passwordHash:
            print('Login success!')
            instructions()
        else:
            print('Login failure')
              
master = tk.Tk()
master.geometry('400x150')
master.title('e-voting')

tk.Label(master,foreground='black',font=1,height=1,padx=8,pady=10,anchor='w', 
         text="Login Username").grid(row=2,sticky=tk.W)
tk.Label(master,foreground='black',font=1,height=1,padx=8,pady=10,anchor='w', 
         text="Login Password").grid(row=3,sticky=tk.W)

e3 = tk.Entry(fg='black',bg='yellow',width=20,font=1)
e4 = tk.Entry(fg='black',bg='yellow',width=20,font=1)

e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

tk.Button(master, 
          text='Login',font=1,width=9,bg='red',fg='yellow', 
          activebackground = "red",command=login).grid(row=4, 
                                    column=0, 
                                    sticky=tk.W,
                                    padx=10,
                                    pady=5)

tk.Button(master, 
          text='Instructions',font=1,width=9,bg='red',fg='yellow', 
          activebackground = "red",command=login).grid(row=4, 
                                    column=1, 
                                    sticky=tk.E,
                                    padx=0,
                                    pady=5)


tk.mainloop()


