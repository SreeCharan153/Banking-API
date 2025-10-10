from fastapi import FastAPI, Depends
from fastapi.responses import  JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import Auth
from transaction import Transaction
from updateinfo import Update
from cs import CustmorService
from history import History
from typing import Optional,Any
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import jwt

load_dotenv()
SECRET_KEY:Any = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable not set")
ALGORITHM = "HS256"

app = FastAPI()
auth = Auth()
update = Update()
trs = Transaction()
cs = CustmorService()
his = History()
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
    pin: Optional[str] = None

class ChangePinRequest(AccountBase):
    newpin: str

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

@app.post("/auth/Create-User")
def create_user(un: str,pas: str,vps: str):
    if vps != pas:
        return JSONResponse(
            status_code=400,
            content={"detail": "Password dose not match"}
        )
    token = jwt.encode(
        {"user":un,"exp":datetime.utcnow()+timedelta(minutes=60)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"message": auth.create_employ(un,pas)}
    

@app.post("/check-password/")
def check_password(h: str,pas: str):
    if auth.password_check(h,pas):
        auth.login(h)
        token = jwt.encode(
                {"user": h, "exp": datetime.utcnow() + timedelta(minutes=60)},
                SECRET_KEY, 
                algorithm=ALGORITHM)
        return {"access_token": token, "token_type": "bearer","message": "Password is correct"}
    else:
        return JSONResponse(
            status_code=400,
            content={"detail": "Incorrect password"}
        )

@app.post("/transfor/")
def transfer_amount(data: TransforRequest):
    return {"message": trs.transfor(data.h, data.r, data.amount, data.pin)}

@app.post("/deposit/")
def deposit_amount(data: TransactionRequest):
    s,m = trs.deposit(data.h, data.amount, data.pin)
    return {"message": m}

@app.post("/withdraw/")
def withdraw_amount(data: TransactionRequest):
    s,m = trs.withdraw(data.h, data.amount, data.pin)
    return {"message": m}

@app.post("/create/")
def create_account(data: CreateAccountRequest):
    return {"message": auth.create(data.h, data.pin, data.mobileno, data.gmail)}

@app.post("/update-mobile/")
def update_mobile(data: UpdateMobileRequest):
    return {"message": update.mobile(data.h, data.nmobile, data.omobile)}

@app.post("/enquiry/")
def enquiry(data: AccountBase):
    return{"message": cs.enquiry(data.h,data.pin)}

@app.post("/change-pin/")
def change_pin(data: ChangePinRequest):
    return {"message": update.change_pin(data.h,data.newpin,data.pin)}

@app.post("/update-email/")
def update_email(data: UpdateEmailRequest):
    return {"message": update.email(data.h, data.nemail, data.oemail)}

@app.post("/history/")
def get_history(data: AccountBase):
    history = his.get_history(data.h, data.pin)
    if history:
        return {"history": list(history)}
    else:
        return JSONResponse(
            status_code=404,
            content={"detail": "No history found for this account"}
        )
 