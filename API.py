from fastapi import FastAPI, Depends
from fastapi.responses import  JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from ATM import ATM
from typing import Optional

app = FastAPI()
atm = ATM()
@app.get("/{pas}")
def read_root(pas: str):
    if atm.password_check(pas):
        return {"message": "Password is correct"}
    else:
        return JSONResponse(
            status_code=400,
            content={"detail": "Incorrect password"}
        )

@app.get("/create/")
def create_account(h: str, pin: str, mobileno: str, gmail: str):
    return {"message": atm.create(h.strip(), pin.strip(), mobileno.strip(), gmail.strip())}

@app.get("/deposit/")
def deposit_amount(h: str, amount: int, pin:Optional[int]=None ):
    return {"message": atm.deposit(h.strip(), amount,pin)}

@app.get("/withdraw/")
def withdraw_amount(h: str, amount: int ,pin: Optional[int] = None):
    return {"message": atm.withdraw(h,amount, pin)}

@app.get("/enenquiry/")
def enquiry(h: str,pin: int):
    return {"message": atm.enquiry(h,pin)}

@app.get("/update-mobile/")
def update_mobile(h: str, nmobile: str, omobile: str):
    return {"message": atm.mobile(h, nmobile, omobile)}

@app.get("/update-email/")
def update_email(h: str, nemail: str, oemail: str):
    return {"message": atm.email(h, nemail, oemail)}