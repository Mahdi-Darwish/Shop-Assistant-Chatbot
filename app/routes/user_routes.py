from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.core.security import create_access_token,verify_password
from app.dependencies import get_db,get_current_user
from app.schemas.user_schema import Token,UserLogin,UserOut,UserSignup
from app.services.user_services import get_user_by_username,create_user
from app.core.rate_limit import limiter
router = APIRouter(tags=["user"])

@router.post("/signup",response_model=Token,status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def signup(request:Request,payload:UserSignup,db:Session=Depends(get_db)):
    if get_user_by_username(db,payload.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already taken")
    user = create_user(db,username=payload.username,password=payload.password,phone=payload.phone)
    access_token = create_access_token({"sub":user.username})
    return Token(access_token=access_token)

@router.post("/login",response_model=Token)
@limiter.limit("5/minute")
def login(request:Request,payload:UserLogin,db:Session=Depends(get_db)):
    user = get_user_by_username(db,payload.username)
    if not user or not verify_password(payload.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid username or password")
    access_token = create_access_token(data={"sub":user.username})
    return Token (access_token=access_token)

@router.get("/me",response_model=UserOut)
@limiter.limit("30/minute")
def read_current_user(request:Request,current_user=Depends(get_current_user)):
    return current_user