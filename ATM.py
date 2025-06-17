import random
import string
class ATM:
    def ac(self):
        with open("Accounts List.txt") as a:
            l=a.readlines()
            b=l[-1].strip()
            l1=b.split(':')
            l2=l1[1].split('AC')
            l1[1]='AC'+str(int(l2[1])+1)
            return l1[1]
    def create(self):
        try:
            holder=input("ENTER ACCOUNT HOLDER NAME:  ")
            pin=int(input("CREATE NEW PIN: "))
            pin=str(pin)
            if len(pin)!=4:
                raise KeyError('PIN MUST BE 4 DIGITS')
            mobileno=input("ENTER MOBILE NUMBER:")
            if len(mobileno)!=10:
                raise KeyError('INVALIED MOBILE NUMBER')
            gmail=input("ENTER GMAIL:")
            if '@' not in gmail:
                raise KeyError('INVALIED EMAIL ID')
            b=self.ac()
            file=b+".txt"
            with open("default.txt") as d,open(file,'x') as h:
                l1=d.readlines()
                h.writelines(l1)
            with open(file) as h,open('Accounts List.txt','a') as acc:
                l=h.readlines()
                acc.writelines(holder+':'+b+'\n')
        except FileExistsError:
            print("*"*5,'HOLDER ALREADY EXISTS PLEASE CHOOSE ANOTHER NAME','*'*5)
        except KeyError as a:
            print('*'*5,a,'*'*5)
        else:
            l[0]='ACCOUNT HOLDER:'+holder+'\n'
            l[1]='PIN:'+pin+'\n'
            l[2]='MOBILE NO:'+mobileno+'\n'
            l[3]='EMAIL ID:'+gmail+'\n'
            with open(file,'w+') as h:
                h.writelines(l)
            print("ACCOUNT CREATED with",l[4])
            print("YOUR ACCOUNT NUMNBER IS",b)
    def deposit(self):
        holder=input("ENTER ACCOUNT NUMBER:  ")
        state=self.check(h=holder)
        if state==True:
            file='./'+holder+".txt"
            with open(file) as h:
                l=h.readlines()
            l1=l[4].split(':')
            self.balance=int(l1[1])
            amount=int(input("Enter the amount to deposit: "))
            self.balance=self.balance+amount
            print("New Balance is",self.balance)
            with open(file,'r') as h:
                l=h.readlines()
            l[4]='BALANCE:'+str(self.balance)+'\n'
            with open(file,'w+') as h:
                h.writelines(l)
        elif state==False:
            print('*'*5,"WRONG PASSWORD",'*'*5)
    def withdraw(self):
        holder=input("ENTER ACCOUNT NUMBER:")
        state=self.check(h=holder)
        if state==True:
            file='./'+holder+'.txt'
            with open(file) as h:
                l=h.readlines()
            l1=l[4].split(':')
            self.balance=int(l1[1])
            amount=int(input("Enter the amount to withdraw:"))
            if self.balance<amount:
                print("Insufficient Balance")
            else:
                self.balance=self.balance-amount
                print("New Balance is",self.balance)
                with open(file,'r') as h:
                    l=h.readlines()
                l[4]='BALANCE:'+str(self.balance)+'\n'
                with open(file,'w+') as h:
                    h.writelines(l)
        else:
            print('*'*5,"WRONG PASSWORD",'*'*5)
    def enquiry(self):
        holder=input("ENTER ACCOUNT NUMBER:")
        state=self.check(h=holder)
        if state==True:
            file='./'+holder+'.txt'
            with open(file,'r') as h:
                l=h.readlines()
            print(l[4])
        else:
            print('*'*5,"WRONG PASSWORD",'*'*5)
    def check(self,h):
        pin=int(input('ENTER PIN:'))
        file='./'+h+".txt"
        try:
            with open(file) as h:
                l=h.readlines()
        except:
            print('*'*5,"HOLDER NOT FOUND",'*'*5)
        else:
            l1=l[1].split(':')
            if(pin==int(l1[1])):
                return True
            else:
                return False
    def update(self):
        holder=input("ENTER ACCOUNT NUMBER:  ")
        state=self.check(h=holder)
        if state==True:
            option=int(input("Enter\n1.FOR MOBILE NUMBER\n2.FOR EMAIL ID\n"))
            match option:
                case 1:
                    self.mobile(h=holder)
                case 2:
                    self.email(h=holder)
    def mobile(self,h):
        nmobile=input("ENTER NEW MOBILE NUMBER")
        omobile=input("ENTER OLD MOBILE NUMBER")
        c= self.captcha()
        omobile=omobile+'\n'
        file='./'+h+'.txt'
        with open(file,'r') as h:
            l=h.readlines()
        l1=l[2].split(':')
        if l1[1]==omobile and c==True:
            l[2]='MOBILE NO:'+nmobile+'\n'
            with open(file,'w+') as h:
                h.writelines(l)
                h.seek(0)
                l=h.readlines()
            print("MOBILE NUMBER UPDATED TO",nmobile)
        else:
            print('*'*5,'ACCESS DENIED','*'*5)
            print('*'*5,'MOBILE NUMBER OR CAPTCHA DOSE NOT MATCH','*'*5)
    def email(self,h):
        nemail=input("ENTER NEW EMAIL ID")
        oemail=input("ENTER OLD EMAIL ID")
        c=self.captcha()
        oemail=oemail+'\n'
        file=h+'.txt'
        with open(file,'r') as h:
            l=h.readlines()
        l1=l[3].split(':')
        if l1[1]==oemail and c==True:
            l[3]='EMAIL ID:'+nemail+'\n'
            with open(file,'w+') as h:
                h.writelines(l)
            print("GMAIL UPDATED TO",nemail)
        else:
             print('*' * 5, 'ACCESS DENIED', '*' * 5)
             print('*' * 5, 'EMAILID OR CAPTCHA DOSE NOT MATCH', '*' * 5)
    def password_check(self,pw):
        with open('./Password.txt') as f:
            password=f.read()
        if password==pw:
            return True
        else:
            return False
    def captcha(self):
        char=string.ascii_letters+string.digits
        capt =''.join(random.choice(char) for _ in range(6))
        print('*'*5,'Human Verfication Pending','*'*5)
        print("Captcha is",capt)
        user =input("Enter The Captcha:")
        if(capt==user):
            return True
        else:
            return  False