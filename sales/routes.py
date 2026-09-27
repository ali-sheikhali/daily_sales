from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.sales.schemas import *
from app.sales.models import SalesModels
from app.stores.models import StoresModel


router= APIRouter(tags=["sales"], prefix="/sales")


@router.post("")
async def create_new_sales(request: SalesCreateSchema , db: Session = Depends(get_db)):

    check_store = db.query(StoresModel).filter_by(id = request.store_id).first()

    if not check_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store not found")

    sales = SalesModels(
        amount = request.amount,
        store_id = request.store_id
    )

    db.add(sales)
    db.commit()

    return sales

@router.get("", response_model=List[SalesAllSalesSchema])
async def get_all_sales(db: Session = Depends(get_db)):

    get_sales = db.query(SalesModels).all()

    if not get_sales:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="not any sales")

    return get_sales


@router.get("/{store_id}", response_model=List[SalesWithStoreResponseSchema])
async def get_store_sales(store_id: int = Path(..., gt= 0),db : Session = Depends(get_db)):
    check_store = db.query(StoresModel).filter_by(id = store_id).first()

    if not check_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="store not found")

    get_store_sales_all = db.query(SalesModels).filter_by(store_id = check_store.id).all()

    return get_store_sales_all


@router.put("/{store_id}/{sale_id}")
async def update_store_sales(request: SalesStoreUpdateSchema, store_id: int = Path(..., gt= 0),
                             sale_id: int = Path(gt= 0),
                             db : Session = Depends(get_db)):
    check_store = db.query(StoresModel).filter_by(id = store_id).first()
    
    if not check_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="store not found")

    sale = db.query(SalesModels).filter(
        SalesModels.store_id == check_store.id,
        SalesModels.id == sale_id
    ).first()

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="sale not found"
        )

    sale.amount = request.amount
    sale.sales_date = request.sales_date

    db.commit()
    db.refresh(sale)

    return sale

