from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.users.dependencies import get_current_user
from app.stores.models import StoresModel
from app.store_manager.models import StoreManagerModels

def check_store_access(
    store_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    store = db.query(StoresModel).filter(
        StoresModel.id == store_id
    ).first()

    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found",
        )

    
    if store.owner_id == current_user.id:
        return store

    assignment = db.query(StoreManagerModels).filter(
        StoreManagerModels.store_id == store_id,
        StoreManagerModels.owner_id == current_user.id,
        StoreManagerModels.is_active.is_(True),
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this store",
        )

    return store