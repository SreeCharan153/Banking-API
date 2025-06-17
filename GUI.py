from tkinter import*
from ATM import*
a=ATM()
w=Tk()
w.geometry('800x800')
c=Button(w,text='Create',font=20,command=a.create)
c1=Button(w,text='Update',font=20,command=a.update)
c2=Button(w,text='Deposit',font=20,command=a.deposit)
c3=Button(w,text='Withdrawl',font=20,command=a.withdraw)
c.place(x=10,y=120)
c1.place(x=110,y=120)
c2.place(x=220,y=120)
c3.place(x=330,y=120)
w.mainloop()