import sqlite3
from history import History
from auth import Auth

class Transaction:
    history=History() 
    auth = Auth()
    def deposit(self,ac_no, amount, pin):
            if pin == "bypass":
                state = True
                m = "Transforing amount to account"
            else:
                state, m = self.auth.check(ac_no=ac_no, pin=pin)
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
                if pin != "bypass":
                    try:
                        self.history.add_entry(ac_no, "Deposited", amount)
                    except Exception as e:
                        return (False, f"Error adding history entry: {str(e)}")
                return (True, f"Transaction successful! New Balance: ₹{new_balance}")
            else:
                return m
            
    def withdraw(self,ac_no,amount, pin,s =False):
        state,m=self.auth.check(ac_no=ac_no, pin=pin)
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
                if not s:
                    self.history.add_entry(ac_no, "Withdrawn", amount)
            return (True, f"Transaction successful! New Balance: ₹{new_balance}")
        else:
            return(m)

    def transfor(self,sender,receiver,amount,pin):
        s,m = self.withdraw(sender, amount, pin,True)
        if not s:
            return str(m)
        s,m =  self.deposit(receiver, amount, "bypass")
        if not s:
            self.deposit(sender, amount, pin)
            return str(m)
        self.history.add_entry(sender, f"Transfored to {receiver}", amount)
        self.history.add_entry(receiver, f"Received from {sender}", amount)
        return f"₹{amount} Transferred from {sender} to {receiver}"