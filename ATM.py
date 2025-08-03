import random
import string
class ATM:
    def ac(self):
        with open("Accounts List.txt") as a:
            l=a.readlines()[-1].strip()
            l=l.split(':')[1]
            l=l.strip('AC')
            l='AC'+str(int(l)+1)
            return l
        

    def create(self):
        try:
            holder=input("ENTER ACCOUNT HOLDER NAME:  ")
            pin=input("CREATE NEW PIN: ")
            if len(pin)!=4 or not pin.isdigit():
                raise KeyError('PIN MUST BE 4 DIGITS')
            mobileno=input("ENTER MOBILE NUMBER:")
            if len(mobileno)!=10 or not mobileno.isdigit():
                raise KeyError('INVALIED MOBILE NUMBER')
            gmail=input("ENTER GMAIL:")
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
            self.balance=int(l[4].split(':')[1].strip())
            if self.balance<0:
                print("Balance is negative, please deposit first.")
                return
            while True:
                try:
                    amount=int(input("Enter the amount to deposit: "))
                    if amount <= 0:
                        raise ValueError("Amount must be greater than zero.")
                except ValueError as e:
                    print('*'*5, e, '*'*5)
                else:
                    break
            self.balance=self.balance+amount
            l[4]='BALANCE:'+str(self.balance)+'\n'
            with open(file,'w+') as h:
                h.writelines(l)
            print(f"Transaction successful! New Balance: ₹{self.balance}")
        elif state==False:
            print('*'*5,"WRONG PASSWORD",'*'*5)


    def withdraw(self):
        holder=input("ENTER ACCOUNT NUMBER:")
        state=self.check(h=holder)
        if state==True:
            file='./'+holder+'.txt'
            with open(file) as h:
                l=h.readlines()
            self.balance=int(l[4].split(':')[1].strip())
            if self.balance<=0:
                print("Balance is negative or Zero, please deposit first.")
                return
            try:
                amount=int(input("Enter the amount to withdraw:"))
            except ValueError:
                print('*'*5, "Invalid input. Please enter a numeric amount.", '*'*5)
            else:
                if self.balance<amount:
                    print("Insufficient Balance")
                elif amount <= 0:
                    print('*'*5, "Amount must be greater than zero.", '*'*5)
                else:
                    self.balance=self.balance-amount
                    l[4]='BALANCE:'+str(self.balance)+'\n'
                    with open(file,'w+') as h:
                        h.writelines(l)
                    print(f"Transaction successful! New Balance: ₹{self.balance}")
        else:
            print('*'*5,"WRONG PASSWORD",'*'*5)


    def enquiry(self):
        holder=input("ENTER ACCOUNT NUMBER:")
        state=self.check(h=holder)
        if state==True:
            file='./'+holder+'.txt'
            with open(file,'r') as h:
                l=h.readlines()[4]
            print("ACCOUNT"+l.strip())
        else:
            print('*'*5,"WRONG PASSWORD",'*'*5)


    def check(self,h):
        file='./'+h+".txt"
        try:
            with open(file) as h:
                l=h.readlines()[1]
        except:
            print('*'*5,"HOLDER NOT FOUND",'*'*5)
            return False
        else:
            l=l.split(':')[1]
            for _ in range(3):
                try:
                    pin=int(input('ENTER YOUR PIN:'))
                    if(pin==int(l)):
                        return True
                except ValueError:
                    print("Invalid input. Please enter a numeric PIN.")
        return False
    

    def update(self):
        holder=input("ENTER ACCOUNT NUMBER:  ")
        state=self.check(h=holder)
        if state==True:
            while True:
                try:
                    option=int(input("Enter\n1.FOR MOBILE NUMBER\n2.FOR EMAIL ID\n"))
                    if option not in [1, 2]:
                        raise ValueError("Invalid option. Please enter 1 or 2.")
                except ValueError as e:
                    print('*'*5, e, '*'*5)
                else:
                    break
            match option:
                case 1:
                    self.mobile(h=holder)
                case 2:
                    self.email(h=holder)


    def mobile(self,h):
        while True:
            try:
                nmobile = input("ENTER NEW MOBILE NUMBER: ")
                omobile=input("ENTER OLD MOBILE NUMBER: ")
                if len(nmobile) != 10 or not nmobile.isdigit() or len(omobile) != 10 or not omobile.isdigit():
                    raise ValueError("Invalid mobile number. It must be 10 digits.")
                elif nmobile == omobile:
                    raise ValueError("New mobile number cannot be the same as the old one.")
                break
            except ValueError as e:
                print('*' * 5, e, '*' * 5)
        c= self.captcha()
        file='./'+h+'.txt'
        with open(file,'r') as h:
            l=h.readlines()
        l1=l[2].split(':')[1].strip()
        if l1==omobile.strip() and c:
            l[2]='MOBILE NO:'+nmobile+'\n'
            with open(file,'w') as h:
                h.writelines(l)
            print("MOBILE NUMBER UPDATED TO",nmobile)
        else:
            print('*'*5,'ACCESS DENIED','*'*5)
            print('*'*5,'MOBILE NUMBER OR CAPTCHA DOSE NOT MATCH','*'*5)


    def email(self,h):
        while True:
            try:
                nemail=input("ENTER NEW EMAIL ID: ").lower().strip()
                oemail=input("ENTER OLD EMAIL ID: ").lower().strip()
                if '@' not in nemail or '@' not in oemail:
                    raise ValueError("Invalid email format. Please include '@'.")
                elif nemail == oemail:
                    raise ValueError("New email cannot be the same as the old one.")
                break
            except ValueError as e:
                print('*' * 5, e, '*' * 5)
        c=self.captcha()
        file=h+'.txt'
        with open(file,'r') as h:
            l=h.readlines()
        l1=l[3].split(':')[1].strip().lower()
        if l1==oemail and c:
            l[3]='EMAIL ID:'+nemail+'\n'
            with open(file,'w') as h:
                h.writelines(l)
            print("GMAIL UPDATED TO",nemail)
        else:
             print('*' * 5, 'ACCESS DENIED', '*' * 5)
             print('*' * 5, 'EMAILID OR CAPTCHA DOSE NOT MATCH', '*' * 5)


    def password_check(self,pw):
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