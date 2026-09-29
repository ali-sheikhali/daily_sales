from fastapi import APIRouter, HTTPException, status, Path, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.expenses.models import ExpensesModels
from app.expenses.schemas import *

router = APIRouter(tags=["expenses"], prefix="/expenses")

#  get all expenses
@router.get("", response_model=List[ExpensesGetAllResponseSchemas])
async def get_all_expenses(db: Session = Depends(get_db)):
    result = db.query(ExpensesModels).all()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="expenses is empty")

    return result

# create new expense
@router.post("")
async def create_new_expenses(request: ExpensesCreateRequestSchemas, db: Session = Depends(get_db)):
    new_expense = ExpensesModels(
        store_id=request.store_id,
        amount=request.amount,
        description=request.description
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "expense created successfully",
        },
    )

# get expense by store_id
@router.get("/{store_id}")
async def get_expenses_by_store_id(store_id: int, db: Session = Depends(get_db)):
    result = db.query(ExpensesModels).filter(ExpensesModels.store_id == store_id).all()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found for the specified store"
        )

    return result