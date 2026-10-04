from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.store_manager.schemas import *
from app.store_manager.models import StoreManagerModels
from app.stores.models import StoresModel
from app.users.models import UserModels
from app.users.dependencies import get_current_user

router = APIRouter(tags=["store manager"], prefix="/store-manager")


@router.get("/all" , response_model=List[StoreManagerListSchema])
async def store_manager_list(
    db: Session = Depends(get_db),
    current_user: UserModels = Depends(get_current_user)
    ):
    all_store_managers = db.query(StoreManagerModels).filter_by(owner_id = current_user.id).all()

    if not all_store_managers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not store managers find")

    return all_store_managers


@router.post("/new")
async def create_new_store_manager(
    request: StoreManagerCreateSchema,
    db: Session = Depends(get_db),
    current_user: UserModels = Depends(get_current_user)
    ):

    check_store = db.query(StoresModel).filter_by(
         id=request.store_id,
         owner_id=current_user.id
         ).first()
    
    if not check_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="store not found")

    new_manager = StoreManagerModels(
        owner_id= current_user.id,
        store_id=request.store_id
    )

    db.add(new_manager)
    db.commit()
    db.refresh(new_manager)

    return new_manager


@router.put("/{store_manager_id}")
async def update_store_manager(
    store_manager_id: int,
    request: StoreManagerUpdate,
    db: Session = Depends(get_db),
    current_user: UserModels = Depends(get_current_user)
):
    store_manager = db.query(StoreManagerModels).filter_by(
    id=store_manager_id,
    owner_id=current_user.id,
).first()

    if not store_manager:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="store manager not found")

    check_store = db.query(StoresModel).filter_by(
        id=request.store_id,
        owner_id=current_user.id,
    ).first()

    if not check_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="store not found")

    store_manager.store_id = request.store_id
    store_manager.is_active = request.is_active

    db.commit()
    db.refresh(store_manager)
    return store_manager