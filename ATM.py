import random
import string

class ATM:
    def __init__(self) -> None:
        pass
    
    
    def ac(self):
        with open("Accounts List.txt") as a:
            l=a.readlines()[-1].strip()
            l=l.split(':')[1]
            l=l.strip('AC')
            l='AC'+str(int(l)+1)
            return l
    
    def transfor(self,sender,receiver,amount,pin):
        s,m = self.withdraw(sender, amount, pin)
        if not s:
            return m
        s,m =  self.deposit(receiver, amount, "bypass")
        if not s:
            self.deposit(sender, amount, "bypass")
            return m
        return f"₹{amount} Transferred from {sender} to {receiver}"

    def create(self,holder,pin,mobileno,gmail):
        try:
            if len(pin)!=4 or not pin.isdigit():
                raise KeyError('PIN MUST BE 4 DIGITS')
            if len(mobileno)!=10 or not mobileno.isdigit():
                raise KeyError('INVALIED MOBILE NUMBER')
            if '@' not in gmail:
                raise KeyError('INVALIED EMAIL ID')
            b=self.ac()
            file = f"./Accounts/{b}.txt"
            with open("./Accounts/default.txt") as d,open(file,'x') as h:
                l1=d.readlines()
                h.writelines(l1)
            with open(file) as h,open('Accounts List.txt','a') as acc:
                l=h.readlines()
                acc.writelines(holder+':'+b+'\n')
        except KeyError as a:
            return(a)
        else:
            l[0]='ACCOUNT HOLDER:'+holder+'\n'
            l[1]='PIN:'+pin+'\n'
            l[2]='MOBILE NO:'+mobileno+'\n'
            l[3]='EMAIL ID:'+gmail+'\n'
            with open(file,'w+') as h:
                h.writelines(l)
            return("ACCOUNT CREATED with",l[4],"\nYOUR ACCOUNT NUMNBER IS",b)


    def deposit(self,holder, amount, pin):
        if pin == "bypass":
            state = True
            m = "Transforing amount to account"
        else:
            state, m = self.check(h=holder, pin=pin)
        if state :
            file = f"./Accounts/{holder}.txt"
            with open(file) as f:
                l=f.readlines()
            self.balance=int(l[4].split(':')[1].strip())
            if self.balance<0:
                return (False,"Balance is negative, please deposit first.")
            if amount <= 0:
                return (False,"Amount must be greater than zero.")
            self.balance=self.balance+amount
            l[4]='BALANCE:'+str(self.balance)+'\n'
            with open(file,'w+') as f:
                f.writelines(l)
            return(True,f"Transaction successful! New Balance: ₹{self.balance}")
        else:
            return m


    def withdraw(self,holder,amount, pin):
        state,m=self.check(h=holder, pin=pin)
        if state==True:
            file = f"./Accounts/{holder}.txt"
            with open(file) as h:
                l=h.readlines()
            self.balance=int(l[4].split(':')[1].strip())
            if self.balance<=0:
                return(False,"Balance is negative or Zero, please deposit first.")
            else:
                if self.balance<amount:
                    return(False,"Insufficient Balance")
                elif amount <= 0:
                    return(False,"Amount must be greater than zero.")
                else:
                    self.balance=self.balance-amount
                    l[4]='BALANCE:'+str(self.balance)+'\n'
                    with open(file,'w+') as h:
                        h.writelines(l)
                    return(True,f"Transaction successful! New Balance: ₹{self.balance}")
        else:
            return(m)


    def enquiry(self,holder,pin):
        state,m=self.check(h=holder,pin=pin)
        if state==True:
            file = f"./Accounts/{holder}.txt"
            with open(file,'r') as h:
                l=h.readlines()[4]
            return("ACCOUNT Balance:"+l.strip())
        else:
            return m


    def check(self,h, pin=None):
        file = f"./Accounts/{h}.txt"
        try:
            with open(file) as h:
                l=h.readlines()[1]
        except:
            return (False,"HOLDER NOT FOUND in check")
        else:
            l=l.split(':')[1]
            try:
                if pin is None:
                    return (False,"PIN NOT PROVIDED")
                elif(pin==int(l)):
                    return (True,"PIN MATCHED")
                else:
                    return (False,"WRONG PIN")
            except ValueError:
                return(False,"Invalid input. Please enter a numeric PIN.")

    def change_pin(self,h,new_pin,old_pin):
        new_pin = str(new_pin)
        old_pin = str(old_pin)
        try:
            if len(new_pin) != 4 or not new_pin.isdigit():
                raise ValueError("PIN must be 4 digits.")
            elif new_pin == old_pin:
                raise ValueError("New PIN cannot be the same as the old one.")
        except ValueError as e:
            return e
        file = f"./Accounts/{h}.txt"
        with open(file,'r') as h:
            l=h.readlines()
        l1=l[1].split(':')[1].strip()
        if l1==old_pin:
            l[1]='PIN:'+new_pin+'\n'
            with open(file,'w') as h:
                h.writelines(l)
            return "PIN UPDATED TO "+new_pin
        else:
            return 'ACCESS DENIED\nPIN DOSE NOT MATCH'

    def mobile(self,h,nmobile,omobile):
        try:
            if len(nmobile) != 10 or not nmobile.isdigit() or len(omobile) != 10 or not omobile.isdigit():
                raise ValueError("Invalid mobile number. It must be 10 digits.")
            elif nmobile == omobile:
                raise ValueError("New mobile number cannot be the same as the old one.")
        except ValueError as e:
            return(e)
        #c= self.captcha()
        file = f"./Accounts/{h}.txt"
        with open(file,'r') as h:
            l=h.readlines()
        l1=l[2].split(':')[1].strip()
        if l1==omobile.strip() :
            l[2]='MOBILE NO:'+nmobile+'\n'
            with open(file,'w') as h:
                h.writelines(l)
            return(f"MOBILE NUMBER UPDATED TO {nmobile}")
        else:
            return(f'ACCESS DENIED\nMOBILE NUMBER OR CAPTCHA DOSE NOT MATCH')


    def email(self,h,nemail,oemail):
        try:
            if '@' not in nemail or '@' not in oemail:
                raise ValueError("Invalid email format. Please include '@'.")
            elif nemail == oemail:
                raise ValueError("New email cannot be the same as the old one.")
        except ValueError as e:
            return(e)
        #c=self.captcha()
        file = f"./Accounts/{h}.txt"
        with open(file,'r') as h:
            l=h.readlines()
        l1=l[3].split(':')[1].strip().lower()
        if l1==oemail:
            l[3]='EMAIL ID:'+nemail+'\n'
            with open(file,'w') as h:
                h.writelines(l)
            return("GMAIL UPDATED TO",nemail)
        else:
            return(f'ACCESS DENIED\nEMAILID OR CAPTCHA DOSE NOT MATCH')


    def password_check(self,h,pw):
        if h != "admin":
            with open(f"./Accounts/{h}.txt") as f:
                l=f.readlines()[1]
                return l.split(':')[1].strip() == pw
        else:
            with open('./Password.txt') as f:
                password=f.read().strip()
            return pw == password
        

    def captcha(self):
        for _ in range(3):
            char=string.ascii_letters+string.digits
            capt =''.join(random.choice(char) for _ in range(6))
            print('*'*5,'Human Verfication Pending','*'*5)
            print("Captcha is",capt)
            user =input("Enter The Captcha:")
            if user != capt:
                print('*' * 5, 'WRONG CAPTCHA', '*' * 5)
            else:
                print('*' * 5, 'CAPTCHA VERIFIED', '*' * 5)
                return True
        return False