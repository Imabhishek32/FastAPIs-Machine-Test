
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import models, auth
from dependencies import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not auth.verify_password(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = auth.create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
