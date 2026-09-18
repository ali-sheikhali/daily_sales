from fastapi import APIRouter, Depends, HTTPException, status
from app.users.schemas import *
from app.users.models import UserModels
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
async def user_login(request: UserLoginSchema , db: Session = Depends(get_db)):
    check_username_match = db.query(UserModels).filter_by(username = request.username).first()

    if not check_username_match:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user not found")
    if not check_username_match.verify_password(request.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="password is invalid")

    return JSONResponse(content={"detail": "login successfully"})


@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    check_user = db.query(UserModels).filter_by(username = request.username).first()

    if check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")

    user_obj = UserModels(username=request.username)
    user_obj.set_password(request.password)

    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"detail": "user register successfully"})