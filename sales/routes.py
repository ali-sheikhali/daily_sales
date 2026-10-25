from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.sales.schemas import *
from app.sales.models import SalesModels
from app.stores.models import StoresModel
from app.users.dependencies import get_current_user
from app.users.permissions import check_store_access

router= APIRouter(tags=["sales"], prefix="/sales", dependencies=[Depends(get_current_user)])

# new sales
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

# get all sales
# @router.get("/{store_id}", response_model=List[SalesAllSalesSchema])
# async def get_all_sales(store_id: int = Path(..., gt= 0), db: Session = Depends(get_db)):

#     get_sales = db.query(SalesModels).filter(SalesModels.store_id == store_id).all()

#     if not get_sales:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="sales not found")

#     return get_sales

# get sales by store
@router.get("/{store_id}", response_model=List[SalesWithStoreResponseSchema])
async def get_store_sales(store_id: int = Path(..., gt= 0),
                          store: StoresModel = Depends(check_store_access),
                          db : Session = Depends(get_db)):
    check_store = db.query(StoresModel).filter_by(id = store_id).first()

    if not check_store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="store not found")

    get_store_sales_all = db.query(SalesModels).filter_by(store_id = check_store.id).all()

    return get_store_sales_all

# update sales
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

# delete sales  
@router.delete("/{store_id}/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store_sale(store_id: int = Path(..., gt=0) , sale_id: int  = Path(..., gt=0) , db: Session = Depends(get_db)):

    if not db.get(StoresModel, store_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="store not found")

    sale = db.query(SalesModels).filter(SalesModels.id == sale_id, SalesModels.store_id == store_id).first()

    if not sale:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Sale not found")

    db.delete(sale)
    db.commit()
    