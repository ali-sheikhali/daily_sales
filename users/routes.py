from fastapi import APIRouter, Depends, HTTPException, status
from app.users.schemas import *
from app.users.models import UserModels
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.core.security import create_access_token


router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
async def user_login(request: UserLoginSchema , db: Session = Depends(get_db)):
    user = db.query(UserModels).filter_by(username = request.username).first()

    if not user or not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    token = create_access_token(user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    check_user = db.query(UserModels).filter_by(username = request.username).first()

    if check_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user already exists")

    user_obj = UserModels(username=request.username, role=request.role)
    user_obj.set_password(request.password)

    db.add(user_obj)
    db.commit()
    return JSONResponse(content={"detail": "user register successfully"})