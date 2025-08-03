from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
from ATM import ATM

app = FastAPI()
@app.get("/{pas}")
def read_root(pas: str):
    atm = ATM()
    if atm.password_check(pas):
        return {"message": "Password is correct"}
    else:
        return JSONResponse(
            status_code=400,
            content={"detail": "Incorrect password"}
        )
