from tkinter import *
from tkinter import messagebox,filedialog
from tkinter import ttk
import time
import sqlite3
import pandas as pd

root = Tk()
root.title('Student Management System')
root.config(bg='gold2')
root.geometry('1174x700+200+50')
# root.iconbitmap('mana.ico')
root.resizable(False,False)

def tick():
    time_string = time.strftime("%H:%M:%S")
    date_string = time.strftime("%d/%m/%Y")
    clock.config(text='Date :'+date_string+"\n"+"Time : "+time_string)
    clock.after(200,tick)

def connect():
    def connect_sub():
        try:
            if passwordval.get()=="123" and hostval.get()=="javed":
                conn=sqlite3.connect("Student_Databse.db")
                cr=conn.cursor()
                messagebox.showinfo("Database Connection","Student Database Connected Successfully")
                # cr.execute('''CREATE TABLE students(id integer PRIMARY KEY NOT NULL,name text,mobile text,email text,address text,gender text,dob text,date text,time text) ''')
                conn.commit()
                conn.close()     
            else:
                messagebox.showerror("Database Connection","Invalid Credentials")

        except:
            messagebox.showerror("Database Connection","Invalid Credentials!!Try Again")



    dbroot = Toplevel()
    dbroot.grab_set()
    dbroot.geometry('470x250+800+230')
    dbroot.resizable(False,False)
    dbroot.config(bg='blue')

    hostlabel = Label(dbroot,text="Enter Host : ",bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=13,anchor='w')
    hostlabel.place(x=10,y=10)

    userlabel = Label(dbroot,text="Enter User : ",bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=13,anchor='w')
    userlabel.place(x=10,y=70)

    passwordlabel = Label(dbroot,text="Enter Password : ",bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=13,anchor='w')
    passwordlabel.place(x=10,y=130)

    hostval = StringVar()
    userval = StringVar()
    passwordval = StringVar()

    hostentry = Entry(dbroot,font=('roman',15,'bold'),bd=5,textvariable=hostval)
    hostentry.place(x=250,y=10)

    userentry = Entry(dbroot,font=('roman',15,'bold'),bd=5,textvariable=userval)
    userentry.place(x=250,y=70)

    passwordentry = Entry(dbroot,font=('roman',15,'bold'),bd=5,textvariable=passwordval)
    passwordentry.place(x=250,y=130)

    submitbutton = Button(dbroot,text='Submit',font=('roman',15,'bold'),bg='red',bd=5,width=20,activebackground='blue',
                          activeforeground='white',command=connect_sub)
    submitbutton.place(x=150,y=190)

    dbroot.mainloop()

#############################################
def show():
    conn=sqlite3.connect("Student_Databse.db")
    cr=conn.cursor()      
    data=cr.execute("SELECT * FROM students")
    conn.commit()
    studenttable.delete(*studenttable.get_children())
    for i in data:
        studenttable.insert("",END,values=i)
    conn.close()

def delete():
    content=studenttable.focus()
    content=studenttable.item(content)
    conn=sqlite3.connect("Student_Databse.db")
    cr=conn.cursor()      
    cr.execute("DELETE FROM students WHERE id='"+str(content['values'][0])+"'")
    conn.commit()
    studenttable.delete(studenttable.focus())
    messagebox.showinfo("Data Delete","Data Deleted Successfully")
    conn.close()

def export():
    content=studenttable.get_children()
    idv,name,mob,email,add,gen,dob,date,time=[],[],[],[],[],[],[],[],[]
    for i in content:
        idv.append(studenttable.item(i)["values"][0])
        name.append(studenttable.item(i)["values"][1])
        mob.append(studenttable.item(i)["values"][2])
        email.append(studenttable.item(i)["values"][3])
        add.append(studenttable.item(i)["values"][4])
        gen.append(studenttable.item(i)["values"][5])
        dob.append(studenttable.item(i)["values"][6])
        date.append(studenttable.item(i)["values"][7])
        time.append(studenttable.item(i)["values"][8])
    # print(idv,name,mob,email,add,gen,dob,date,time)
    # print(zip(idv,name,mob,email,add,gen,dob,date,time))
    # print(list(zip(idv,name,mob,email,add,gen,dob,date,time)))
    df=pd.DataFrame(list(zip(idv,name,mob,email,add,gen,dob,date,time)),columns=['ID','Name','Mobile','Email','Address','Gender','DOB','Date','Time'])
    path=filedialog.asksaveasfilename(title="Save")
    # print(path)
    try:
        if path!="":
            df.to_csv(f"{path}.csv",index=False)
            messagebox.showinfo("Data Export","Data Exported Successfully")
    except:
        pass

def add():
    def add_sub():
       id_value= idval.get()
       name= nameval.get()
       mob= mobileval.get()
       email= emailval.get()
       address= addressval.get()
       gender= genderval.get()
       dob= dobval.get()
       addedtime=time.strftime("%H:%M:%S")
       addeddate=time.strftime("%d/%m/%Y")
       try:
            conn=sqlite3.connect("Student_Databse.db")
            cr=conn.cursor()
            
            cr.execute("INSERT INTO students VALUES (?,?,?,?,?,?,?,?,?)",(id_value,name,mob,email,address,gender,dob,addeddate,addedtime))
            conn.commit()
            res=messagebox.askyesno("ADD DATA","Student Added Succesfully, do you want to clear the form?",parent=addroot)
            if res==True:
                idval.set("")
                nameval.set("")
                mobileval.set("")
                emailval.set("")
                addressval.set("")
                genderval.set("")
                dobval.set("")
            conn.close() 
       except:
            messagebox.showerror("Data Error","ID already Exists!!",parent=addroot)

    addroot = Toplevel(master=DataEntryFrame)
    addroot.grab_set()
    addroot.geometry('470x470+220+200')
    addroot.title('Student Management System')
    addroot.config(bg='blue')
    addroot.resizable(False,False)
    #--------------------------------------------------- Add student Labels
    idlabel = Label(addroot,text='Enter Id : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    idlabel.place(x=10,y=10)

    namelabel = Label(addroot,text='Enter Name : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    namelabel.place(x=10,y=70)

    mobilelabel = Label(addroot,text='Enter Mobile : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    mobilelabel.place(x=10,y=130)

    emaillabel = Label(addroot,text='Enter Email : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    emaillabel.place(x=10,y=190)

    addresslabel = Label(addroot,text='Enter Address : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    addresslabel.place(x=10,y=250)

    genderlabel = Label(addroot,text='Enter Gender : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    genderlabel.place(x=10,y=310)

    doblabel = Label(addroot,text='Enter D.O.B : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    doblabel.place(x=10,y=370)

    ##----------------------------------------------------------- Add student Entry
    idval = StringVar()
    nameval = StringVar()
    mobileval = StringVar()
    emailval = StringVar()
    addressval = StringVar()
    genderval = StringVar()
    dobval = StringVar()

    identry = Entry(addroot,font=('roman',15,'bold'),bd=5,textvariable=idval)
    identry.place(x=250,y=10)

    nameentry = Entry(addroot,font=('roman',15,'bold'),bd=5,textvariable=nameval)
    nameentry.place(x=250,y=70)

    mobileentry = Entry(addroot,font=('roman',15,'bold'),bd=5,textvariable=mobileval)
    mobileentry.place(x=250,y=130)

    emailentry = Entry(addroot,font=('roman',15,'bold'),bd=5,textvariable=emailval)
    emailentry.place(x=250,y=190)

    addressentry = Entry(addroot,font=('roman',15,'bold'),bd=5,textvariable=addressval)
    addressentry.place(x=250,y=250)

    genderentry = Entry(addroot,font=('roman',15,'bold'),bd=5,textvariable=genderval)
    genderentry.place(x=250,y=310)

    dobentry = Entry(addroot,font=('roman',15,'bold'),bd=5,textvariable=dobval)
    dobentry.place(x=250,y=370)

    submitbtn = Button(addroot,text='Submit',font=('roman',15,'bold'),width=20,bd=5,activebackground='blue',activeforeground='white',
                      bg='yellow',command=add_sub)
    submitbtn.place(x=150,y=420)

    addroot.mainloop()

def search():
    def search_sub():
        id_value= idval.get()
        name= nameval.get()
        mob= mobileval.get()
        email= emailval.get()
        address= addressval.get()
        gender= genderval.get()
        dob= dobval.get()
        date=dateval.get()

        conn=sqlite3.connect("Student_Databse.db")
        cr=conn.cursor()
        if id_value!="":
            data=cr.execute("SELECT * FROM students WHERE id='"+id_value+"'")
            conn.commit()
        if name!="":
            data=cr.execute("SELECT * FROM students WHERE name='"+name+"'")
            conn.commit()
        if mob!="":
            data=cr.execute("SELECT * FROM students WHERE mobile='"+mob+"'")
            conn.commit()
        if email!="":
            data=cr.execute("SELECT * FROM students WHERE email='"+email+"'")
            conn.commit()
        if address!="":
            data=cr.execute("SELECT * FROM students WHERE address='"+address+"'")
            conn.commit()
        if gender!="":
            data=cr.execute("SELECT * FROM students WHERE gender='"+gender+"'")
            conn.commit()
        if dob!="":
            data=cr.execute("SELECT * FROM students WHERE dob='"+dob+"'")
            conn.commit()
        if date!="":
            data=cr.execute("SELECT * FROM students WHERE date='"+date+"'")
            conn.commit()

        studenttable.delete(*studenttable.get_children())
        for i in data:
            studenttable.insert("",END,values=i)
        conn.close()

    searchroot = Toplevel(master=DataEntryFrame)
    searchroot.grab_set()
    searchroot.geometry('470x540+220+200')
    searchroot.title('Student Management System')
    searchroot.config(bg='firebrick1')
    searchroot.resizable(False,False)
    #--------------------------------------------------- Search Labels
    idlabel = Label(searchroot,text='Enter Id : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    idlabel.place(x=10,y=10)

    namelabel = Label(searchroot,text='Enter Name : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    namelabel.place(x=10,y=70)

    mobilelabel = Label(searchroot,text='Enter Mobile : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    mobilelabel.place(x=10,y=130)

    emaillabel = Label(searchroot,text='Enter Email : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    emaillabel.place(x=10,y=190)

    addresslabel = Label(searchroot,text='Enter Address : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    addresslabel.place(x=10,y=250)

    genderlabel = Label(searchroot,text='Enter Gender : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    genderlabel.place(x=10,y=310)

    doblabel = Label(searchroot,text='Enter D.O.B : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    doblabel.place(x=10,y=370)

    datelabel = Label(searchroot,text='Enter Date : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    datelabel.place(x=10,y=430)

    ##----------------------------------------------------------- Search Entry
    idval = StringVar()
    nameval = StringVar()
    mobileval = StringVar()
    emailval = StringVar()
    addressval = StringVar()
    genderval = StringVar()
    dobval = StringVar()
    dateval = StringVar()

    identry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=idval)
    identry.place(x=250,y=10)

    nameentry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=nameval)
    nameentry.place(x=250,y=70)

    mobileentry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=mobileval)
    mobileentry.place(x=250,y=130)

    emailentry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=emailval)
    emailentry.place(x=250,y=190)

    addressentry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=addressval)
    addressentry.place(x=250,y=250)

    genderentry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=genderval)
    genderentry.place(x=250,y=310)

    dobentry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=dobval)
    dobentry.place(x=250,y=370)

    dateentry = Entry(searchroot,font=('roman',15,'bold'),bd=5,textvariable=dateval)
    dateentry.place(x=250,y=430)
    ############------------------------- add button
    submitbtn = Button(searchroot,text='Submit',font=('roman',15,'bold'),width=20,bd=5,activebackground='blue',activeforeground='white',
                      bg='yellow',command=search_sub)
    submitbtn.place(x=150,y=480)

    searchroot.mainloop()
def update():
    content=studenttable.focus()
    content=studenttable.item(content)
    conn=sqlite3.connect("Student_Databse.db")
    cr=conn.cursor()

    def update_sub():
        id_value= idval.get()
        name= nameval.get()
        mob= mobileval.get()
        email= emailval.get()
        address= addressval.get()
        gender= genderval.get()
        dob= dobval.get()
        
        try:    
            if id_value!="":
                data=cr.execute("UPDATE students SET id ='"+id_value+"' WHERE id='"+str(content['values'][0])+"'")
                conn.commit()
            if name!="":
                data=cr.execute("UPDATE students SET name='"+name+"' WHERE name='"+str(content['values'][1])+"'")
                conn.commit()
            if mob!="":
                data=cr.execute("UPDATE students SET mobile='"+mob+"' WHERE mobile='"+str(content['values'][2])+"'")
                conn.commit()
            if email!="":
                data=cr.execute("UPDATE students SET email='"+email+"' WHERE email='"+str(content['values'][3])+"'")
                conn.commit()
            if address!="":
                data=cr.execute("UPDATE students SET address='"+address+"' WHERE address='"+str(content['values'][4])+"'")
                conn.commit()
            if gender!="":
                data=cr.execute("UPDATE students SET gender='"+gender+"' WHERE gender='"+str(content['values'][5])+"'")
                conn.commit()
            if dob!="":
                data=cr.execute("UPDATE students SET dob='"+dob+"' WHERE dob='"+str(content['values'][6])+"'")
                conn.commit()
            messagebox.showinfo("Data Update","Data Updated Successfully,Please refresh")
    
        except Exception as ex:
            print(ex)
            messagebox.showerror("Data Update","ID cannot be updated")
        finally:
            conn.close()   

    updateroot = Toplevel(master=DataEntryFrame)
    updateroot.grab_set()
    updateroot.geometry('470x585+220+160')
    updateroot.title('Student Management System')
    updateroot.config(bg='firebrick1')
    updateroot.resizable(False,False)
    #---------------------------------------------------  Labels
    idlabel = Label(updateroot,text='Enter Id : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    idlabel.place(x=10,y=10)

    namelabel = Label(updateroot,text='Enter Name : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    namelabel.place(x=10,y=70)

    mobilelabel = Label(updateroot,text='Enter Mobile : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    mobilelabel.place(x=10,y=130)

    emaillabel = Label(updateroot,text='Enter Email : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    emaillabel.place(x=10,y=190)

    addresslabel = Label(updateroot,text='Enter Address : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    addresslabel.place(x=10,y=250)

    genderlabel = Label(updateroot,text='Enter Gender : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    genderlabel.place(x=10,y=310)

    doblabel = Label(updateroot,text='Enter D.O.B : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    doblabel.place(x=10,y=370)

    datelabel = Label(updateroot,text='Enter Date : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    datelabel.place(x=10,y=430)

    timelabel = Label(updateroot,text='Enter Time : ',bg='gold2',font=('times',20,'bold'),relief=GROOVE,borderwidth=3,width=12,anchor='w')
    timelabel.place(x=10,y=490)

    ##----------------------------------------------------------- Entry
    idval = StringVar()
    nameval = StringVar()
    mobileval = StringVar()
    emailval = StringVar()
    addressval = StringVar()
    genderval = StringVar()
    dobval = StringVar()
    dateval = StringVar()
    timeval = StringVar()

    identry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=idval,state=DISABLED)
    identry.place(x=250,y=10)

    nameentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=nameval)
    nameentry.place(x=250,y=70)

    mobileentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=mobileval)
    mobileentry.place(x=250,y=130)

    emailentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=emailval)
    emailentry.place(x=250,y=190)

    addressentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=addressval)
    addressentry.place(x=250,y=250)

    genderentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=genderval)
    genderentry.place(x=250,y=310)

    dobentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=dobval)
    dobentry.place(x=250,y=370)

    dateentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=dateval,state=DISABLED)
    dateentry.place(x=250,y=430)

    timeentry = Entry(updateroot,font=('roman',15,'bold'),bd=5,textvariable=timeval,state=DISABLED)
    timeentry.place(x=250,y=490)

    ##########################################
    idval.set(str(content['values'][0]))
    nameval.set(str(content['values'][1]))
    mobileval.set(str(content['values'][2]))
    emailval.set(str(content['values'][3]))
    addressval.set(str(content['values'][4]))
    genderval.set(str(content['values'][5]))
    dobval.set(str(content['values'][6]))
    dateval.set(str(content['values'][7]))
    timeval.set(str(content['values'][8]))

    ############-------------------------  button
    submitbtn = Button(updateroot,text='Submit',font=('roman',15,'bold'),width=20,bd=5,activebackground='blue',activeforeground='white',
                      bg='yellow',command=update_sub)
    submitbtn.place(x=150,y=540)
    updateroot.mainloop()

def exit():
    res = messagebox.askyesnocancel('Exit','Do you want to exit?')
    if(res == True):
        root.destroy()
#################################################

DataEntryFrame = Frame(root,bg='gold2',relief=GROOVE,borderwidth=5)
DataEntryFrame.place(x=10,y=80,width=500,height=600)
frontlabel = Label(DataEntryFrame,text='--------------Welcome--------------',width=30,font=('arial',22,'italic bold'),bg='gold2')
frontlabel.pack(side=TOP,expand=True)
showallbtn = Button(DataEntryFrame,text='1. Show All Data',width=25,font=('',20,'bold'),bd=6,bg='skyblue3',activebackground='blue',relief=RIDGE,
                activeforeground='white',command=show)
showallbtn.pack(side=TOP,expand=True)

searchbtn = Button(DataEntryFrame,text='2. Search Student',width=25,font=('',20,'bold'),bd=6,bg='skyblue3',activebackground='blue',relief=RIDGE,
                activeforeground='white',command=search)
searchbtn.pack(side=TOP,expand=True)

addbtn = Button(DataEntryFrame,text='3. Add Student',width=25,font=('',20,'bold'),bd=6,bg='skyblue3',activebackground='blue',relief=RIDGE,
                activeforeground='white',command=add)
addbtn.pack(side=TOP,expand=True)

updatebtn = Button(DataEntryFrame,text='4. Update Student',width=25,font=('',20,'bold'),bd=6,bg='skyblue3',activebackground='blue',relief=RIDGE,
                activeforeground='white',command=update)
updatebtn.pack(side=TOP,expand=True)

deletebtn = Button(DataEntryFrame,text='5. Delete Student',width=25,font=('',20,'bold'),bd=6,bg='skyblue3',activebackground='blue',relief=RIDGE,
                activeforeground='white',command=delete)
deletebtn.pack(side=TOP,expand=True)

exportbtn = Button(DataEntryFrame,text='6. Export data',width=25,font=('',20,'bold'),bd=6,bg='skyblue3',activebackground='blue',relief=RIDGE,
                activeforeground='white',command=export)
exportbtn.pack(side=TOP,expand=True)

exitbtn = Button(DataEntryFrame,text='7.  Exit',width=25,font=('',20,'bold'),bd=6,bg='skyblue3',activebackground='blue',relief=RIDGE,
                activeforeground='white',command=exit)
exitbtn.pack(side=TOP,expand=True)

##################################
SliderLabel = Label(root,text="STUDENT RECORDS",font=('',20,'italic bold'),borderwidth=4,width=35,bg='cyan')
SliderLabel.place(x=260,y=0)

#####################################################################
ShowDataFrame = Frame(root,bg='gold2',relief=GROOVE,borderwidth=5)
ShowDataFrame.place(x=550,y=80,width=620,height=600)
#######################################################################
style = ttk.Style()
style.configure('Treeview.Heading',font=('arial',20,'bold'),foreground='blue')
style.configure('Treeview',font=('arial',15,'bold'),background='cyan',foreground='black')

scroll_x = Scrollbar(ShowDataFrame,orient=HORIZONTAL)
scroll_y = Scrollbar(ShowDataFrame,orient=VERTICAL)
studenttable = ttk.Treeview(ShowDataFrame,columns=('Id','Name','Mobile No','Email','Address','Gender','D.O.B','Added Date','Added Time'),
                         yscrollcommand=scroll_y.set,xscrollcommand=scroll_x.set)
scroll_x.pack(side=BOTTOM,fill=X)
scroll_y.pack(side=RIGHT,fill=Y)
scroll_x.config(command=studenttable.xview)
scroll_y.config(command=studenttable.yview)
studenttable.heading('Id',text='Id')
studenttable.heading('Name',text='Name')
studenttable.heading('Mobile No',text='Mobile No')
studenttable.heading('Email',text='Email')
studenttable.heading('Address',text='Address')
studenttable.heading('Gender',text='Gender')
studenttable.heading('D.O.B',text='D.O.B')
studenttable.heading('Added Date',text='Added Date')
studenttable.heading('Added Time',text='Added Time')
studenttable['show'] = 'headings'
studenttable.column('Id',width=100)
studenttable.column('Name',width=200)
studenttable.column('Mobile No',width=200)
studenttable.column('Email',width=300)
studenttable.column('Address',width=200)
studenttable.column('Gender',width=110)
studenttable.column('D.O.B',width=150)
studenttable.column('Added Date',width=170)
studenttable.column('Added Time',width=170)
studenttable.pack(fill=BOTH,expand=1)


############################################################################################################### clock
clock = Label(root,font=('times',14,'bold'),relief=RIDGE,borderwidth=4,bg='lawn green')
clock.place(x=0,y=0)
tick()
################################################################################################################## ConnectDatabaseButton
connectbutton = Button(root,text='Connect To Database',width=18,font=('',19,'italic bold'),relief=RIDGE,borderwidth=4,bg='green2',
                       activebackground='blue',activeforeground='white',command=connect)
connectbutton.place(x=870,y=0)
root.mainloop()