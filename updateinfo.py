import sqlite3
from auth import Auth
class Update:
    auth = Auth()
    def change_pin(self, h, new_pin, old_pin):
        new_pin = str(new_pin).strip()
        old_pin = str(old_pin).strip()

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
            if self.auth.pin_hash(old_pin) != stored_pin_hash:
                return "ERROR: Old PIN does not match."
            new_pin_hash = self.auth.pin_hash(new_pin)
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