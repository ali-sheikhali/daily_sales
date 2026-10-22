from fastapi import APIRouter, Depends, HTTPException, status
from app.users.schemas import *
from app.users.models import UserModels
from app.store_manager.models import StoreManagerModels
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.core.security import create_access_token


router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login", response_model=UserLoginResponseSchema)
async def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user = db.query(UserModels).filter_by(username=request.username).first()

    if not user or not user.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid username or password",
        )

    token = create_access_token(user.id)

    if user.role == "manager":
        store_id = db.query(StoreManagerModels).filter(StoreManagerModels.owner_id == user.id).first()
    else:
        store_id = None

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "access_token": token,
            "token_type": "bearer",
            "username": user.username,
            "role": user.role,
            "id": user.id,
            "store_id": store_id.store_id if store_id else None
        }
    )


@router.post(
    "/register",
    response_model=UserRegisterResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    check_user = db.query(UserModels).filter_by(
        username=request.username).first()

    if check_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="user already exists")

    user_obj = UserModels(username=request.username, role=request.role)
    user_obj.set_password(request.password)

    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)  # loads the generated id

    return user_obj
