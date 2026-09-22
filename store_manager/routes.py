from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.store_manager.schemas import *
from app.store_manager.models import StoreManagerModels
from app.store_manager.models import StoreManagerModels
from app.stores.models import StoresModel
from app.users.models import UserModels

router = APIRouter(tags=["store manager"], prefix="/store-manager")


@router.get("" , response_model=List[StoreManagerListSchema])
async def store_manager_list(db: Session = Depends(get_db)):
    all_store_managers = db.query(StoreManagerModels).all()

    if not all_store_managers:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not store managers find")

    return all_store_managers


@router.post("/new")
async def create_new_store_manager(request: StoreManagerCreateSchema, db: Session = Depends(get_db)):

    check_user = db.query(UserModels).filter_by(id = request.owner_id).first()
    check_store = db.query(StoresModel).filter_by(id = request.store_id).first()

    if not check_user or not check_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="owner or store not found")

    new_manager = StoreManagerModels(
        owner_id=request.owner_id,
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
    db: Session = Depends(get_db)
):
    # 1. Find store manager
    store_manager = (
        db.query(StoreManagerModels)
        .filter_by(id=store_manager_id)
        .first()
    )

    if not store_manager:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="store manager not found"
        )

    # 2. Check owner
    check_user = (
        db.query(UserModels)
        .filter_by(id=request.owner_id)
        .first()
    )

    if not check_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="owner not found"
        )

    # 3. Check store
    check_store = (
        db.query(StoresModel)
        .filter_by(id=request.store_id)
        .first()
    )

    if not check_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="store not found"
        )

    # 4. Update
    store_manager.owner_id = request.owner_id
    store_manager.store_id = request.store_id
    store_manager.is_active = request.is_active

    # 5. Save
    db.commit()
    db.refresh(store_manager)

    return store_manager