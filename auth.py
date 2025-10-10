import sqlite3
from hashlib import sha512
class Auth:
    
    def ac(self):
        with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM accounts')
            count = cursor.fetchone()[0]
            account_no = f'AC1000000{count + 1:04d}'
            return account_no
    
    def pin_hash(self, pin: str) -> str:
        return sha512(pin.encode()).hexdigest()
    
    def login(self, username):
        with sqlite3.connect('./Database/Bank.db', timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM users WHERE user_name = ?', (username,))
            row = cursor.fetchone()
            if row:
                user_id = row[0]
                cursor.execute('INSERT INTO logins (user_id) VALUES (?)', (user_id,))
            conn.commit()
            
    def create_employ(self,username,pas):
        try:
            pas = self.pin_hash(pas)
            with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                            INSERT INTO users(user_name,password)
                           VALUES(?,?)
                           ''',(username,pas))
                conn.commit()
            return f'User created with username:{username}'
        except Exception as e:
            return f'Error:{str(e)}'
        
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
        
    def password_check(self,h,pw):
        with sqlite3.connect('./Database/Bank.db',timeout=10) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE user_name = ?', (h,))
            result = cursor.fetchone()
            if result is None:
                return False
            stored_pin_hash = result[0]
            return(self.pin_hash(pw) == stored_pin_hash)
        
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
        
        
    '''def captcha(self):
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
        return False'''