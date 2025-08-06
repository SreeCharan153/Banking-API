from fastapi import FastAPI, Depends
from fastapi.responses import  JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ATM import ATM
from typing import Optional

app = FastAPI()
atm = ATM()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from typing import Optional
from pydantic import BaseModel, EmailStr


class AccountBase(BaseModel):
    h: str
    pin: Optional[int] = None


class TransactionRequest(AccountBase):
    amount: int

class TransforRequest(TransactionRequest):
    r: str
    
class CreateAccountRequest(BaseModel):
    h: str
    pin: str
    mobileno: str
    gmail: EmailStr

class UpdateMobileRequest(AccountBase):
    nmobile: str
    omobile: str

class UpdateEmailRequest(AccountBase):
    nemail: EmailStr
    oemail: EmailStr
    
@app.get("/")
def read_root():
    return {"message": "Welcome to the ATM API"}

@app.post("/check-password/")
def check_password(h: str,pas: str):
    if atm.password_check(h,pas):
        return {"message": "Password is correct"}
    else:
        return JSONResponse(
            status_code=400,
            content={"detail": "Incorrect password"}
        )

@app.post("/transfor/")
def transfer_amount(data: TransforRequest):
    return {"message": atm.transfor(data.h, data.r, data.amount, data.pin)}

@app.post("/deposit/")
def deposit_amount(data: TransactionRequest):
    s,m = atm.deposit(data.h, data.amount, data.pin)
    return {"message": m}

@app.post("/withdraw/")
def withdraw_amount(data: TransactionRequest):
    s,m = atm.withdraw(data.h, data.amount, data.pin)
    return {"message": m}

@app.post("/create/")
def create_account(data: CreateAccountRequest):
    return {"message": atm.create(data.h, data.pin, data.mobileno, data.gmail)}

@app.post("/update-mobile/")
def update_mobile(data: UpdateMobileRequest):
    return {"message": atm.mobile(data.h, data.nmobile, data.omobile)}

@app.post("/enquiry/")
def enquiry(data: AccountBase):
    return{"message": atm.enquiry(data.h,data.pin)}

@app.post("/update-email/")
def update_email(data: UpdateEmailRequest):
    return {"message": atm.email(data.h, data.nemail, data.oemail)}
