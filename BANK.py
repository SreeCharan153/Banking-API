from ATM import*
p=input("ENTER THE PASSWORD")
a=ATM()
c=a.password_check(pw=p)
if(c==True):
    print('*'*5,"WELCOME TO THE ATM SOFTWARE",'*'*5,sep='')
    while(1):
        option=eval(input("ENTER\n1.FOR CREATING NEW ACCOUNT\n2.FOR DEPOSIT\n3.FOR WITHDRAW\n4.FOR ENQUIRY\n5.FOR UPDATE\n0.FOR EXIT\n"))
        if option==0:
            break
        match option:
            case 1:
                a.create()
            case 2:
                a.deposit()
            case 3:
                a.withdraw()
            case 4: 
                a.enquiry()
            case 5:
                a.update()
            case _:
                print("SORRY OPTION NOT AVELAVLE")
else:
    print('*'*5,"WORNG PASSWORD",'*'*5,sep='')
    print('*'*5,"ACCESS DENIED",'*'*5,sep='')
