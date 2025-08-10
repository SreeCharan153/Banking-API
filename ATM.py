import random
import string
import os
import sqlite3
from hashlib import sha512



class ATM:
    def __init__(self) -> None:
        conn = sqlite3.connect('./Database/Bank.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_no TEXT UNIQUE,
            name TEXT,
            pin TEXT,
            balance REAL DEFAULT 0.0,
            mobileno TEXT,
            gmail TEXT
        )
        ''')
        conn.commit()
        conn.close()
    
    def pin_hash(self, pin: str) -> str:
        return sha512(pin.encode()).hexdigest()
    
    def ac(self):
        with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM accounts')
            count = cursor.fetchone()[0]
            account_no = f'AC1000000{count + 1:04d}'
            return account_no
    
    def transfor(self,sender,receiver,amount,pin):
        s,m = self.withdraw(sender, amount, pin)
        if not s:
            return m
        s,m =  self.deposit(receiver, amount, "bypass")
        if not s:
            self.deposit(sender, amount, pin)
            return m
        return f"₹{amount} Transferred from {sender} to {receiver}"

    def create(self, holder, pin, mobileno, gmail):
        try:
            if len(pin) != 4 or not pin.isdigit():
                raise KeyError('PIN MUST BE 4 DIGITS')
            if len(mobileno) != 10 or not mobileno.isdigit():
                raise KeyError('INVALID MOBILE NUMBER')
            if '@' not in gmail:
                raise KeyError('INVALID EMAIL ID')

            ac_no = self.ac()

            with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO accounts (account_no, name, pin, balance, mobileno, gmail)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (ac_no, holder, self.pin_hash(pin), 0.0, mobileno, gmail))
                conn.commit()

            return f"Account created successfully! Account No: {ac_no}"

        except Exception as e:
            return f"Error: {str(e)}"



    def deposit(self,ac_no, amount, pin):
        if pin == "bypass":
            state = True
            m = "Transforing amount to account"
        else:
            state, m = self.check(ac_no=ac_no, pin=pin)
        if state :
            with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT balance FROM accounts WHERE account_no = ?', (ac_no,))
                result = cursor.fetchone()
                if result is None:
                    return (False, "Account not found.")
                current_balance = result[0]
                if amount <= 0:
                    return (False, "Amount must be greater than zero.")
                new_balance = current_balance + amount
                cursor.execute('UPDATE accounts SET balance = ? WHERE account_no = ?', (new_balance, ac_no))
                conn.commit()
            return (True, f"Transaction successful! New Balance: ₹{new_balance}")
        else:
            return m


    def withdraw(self,ac_no,amount, pin):
        state,m=self.check(ac_no=ac_no, pin=pin)
        if state==True:
            with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT balance FROM accounts WHERE account_no = ?', (ac_no,))
                result = cursor.fetchone()
                if result is None:
                    return (False, "Account not found.")
                current_balance = result[0]
                if amount <= 0:
                    return (False, "Amount must be greater than zero.")
                if current_balance < amount:
                    return (False, "Insufficient funds.")
                new_balance = current_balance - amount
                cursor.execute('UPDATE accounts SET balance = ? WHERE account_no = ?', (new_balance, ac_no))
                conn.commit()
            return (True, f"Transaction successful! New Balance: ₹{new_balance}")
        else:
            return(m)


    def enquiry(self,ac_no,pin):
        state,m=self.check(ac_no=ac_no,pin=pin)
        if state==True:
            with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT balance FROM accounts WHERE account_no = ?', (ac_no,))
                result = cursor.fetchone()
                if result is None:
                    return (False, "Account not found.")
                current_balance = result[0]
            return (True, f"Current Balance: ₹{current_balance}")
        else:
            
            return (m)

    def check(self, ac_no, pin=None):
        try:
            with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT pin FROM accounts WHERE account_no = ?', (ac_no,))
                result = cursor.fetchone()

                if result is None:
                    return (False, "Account not found.")

                stored_pin_hash = result[0]

                if pin is None:
                    return (True, "Account found, no PIN check required.")

                if self.pin_hash(pin) != stored_pin_hash:
                    return (False, "ACCESS DENIED: Incorrect PIN.")

                return (True, "ACCESS GRANTED: PIN is correct.")

        except Exception as e:
            return (False, f"Error during account check: {str(e)}")
   

    def change_pin(self, h, new_pin, old_pin):
        new_pin = str(new_pin).strip()
        old_pin = str(old_pin).strip()

        #  Input validation
        if len(new_pin) != 4 or not new_pin.isdigit():
            return "ERROR: New PIN must be exactly 4 digits."
        if new_pin == old_pin:
            return "ERROR: New PIN cannot be the same as the old PIN."

        with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT pin FROM accounts WHERE account_no = ?', (h,))
            result = cursor.fetchone()
            if result is None:
                return "ERROR: Account not found."
            stored_pin_hash = result[0]
            if self.pin_hash(old_pin) != stored_pin_hash:
                return "ERROR: Old PIN does not match."
            new_pin_hash = self.pin_hash(new_pin)
            cursor.execute('UPDATE accounts SET pin = ? WHERE account_no = ?', (new_pin_hash, h))
            conn.commit()
        return "PIN changed successfully."


    def mobile(self,h,nmobile,omobile):
        try:
            if len(nmobile) != 10 or not nmobile.isdigit() or len(omobile) != 10 or not omobile.isdigit():
                raise ValueError("Invalid mobile number. It must be 10 digits.")
            elif nmobile == omobile:
                raise ValueError("New mobile number cannot be the same as the old one.")
        except ValueError as e:
            return(e)
        #c= self.captcha()
        with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT mobileno FROM accounts WHERE account_no = ?', (h,))
            result = cursor.fetchone()
            if result is None:
                return "ERROR: Account not found."
            old_mobile = result[0]
            if old_mobile == omobile:
                cursor.execute('UPDATE accounts SET mobileno = ? WHERE account_no = ?', (nmobile, h))
                conn.commit()
                return "MOBILE NUMBER UPDATED TO " + nmobile
            else:
                return "ACCESS DENIED\nMOBILE NUMBER OR CAPTCHA DOES NOT MATCH"


    def email(self,h,nemail,oemail):
        try:
            if '@' not in nemail or '@' not in oemail:
                raise ValueError("Invalid email format. Please include '@'.")
            elif nemail == oemail:
                raise ValueError("New email cannot be the same as the old one.")
        except ValueError as e:
            return(e)
        #c=self.captcha()
        with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT gmail FROM accounts WHERE account_no = ?', (h,))
            result = cursor.fetchone()
            if result is None:
                return "ERROR: Account not found."
            old_email = result[0]
            if old_email == oemail:
                cursor.execute('UPDATE accounts SET gmail = ? WHERE account_no = ?', (nemail, h))
                conn.commit()
                return "EMAIL UPDATED TO " + nemail
            else:
                return "ACCESS DENIED\nEMAIL OR CAPTCHA DOES NOT MATCH"


    def password_check(self,h,pw):
            with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT pin FROM accounts WHERE account_no = ?', (h,))
                result = cursor.fetchone()
                if result is None:
                    return False
                stored_pin_hash = result[0]
                print(self.pin_hash(pw) == stored_pin_hash)
            

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