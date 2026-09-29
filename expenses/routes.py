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


# edit expense by id
@router.patch("/{expense_id}", response_model=ExpensesGetAllResponseSchemas)
async def edit_expenses(expense_id: int, request: ExpensesEditRequestSchemas, db: Session = Depends(get_db)):

    expense = db.query(ExpensesModels).filter(ExpensesModels.id == expense_id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="expenses not found"
        )

    update_data = request.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(expense, key, value)

    db.commit()
    db.refresh(expense)
    return expense

# delete expense by id
@router.delete("/{expenses_id}")
async def delete_expense(expenses_id: int, db: Session = Depends(get_db)):
    expense = db.query(ExpensesModels).filter_by(id = expenses_id).first()

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="expense not found"
        )

    db.delete(expense)
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content={"message": "expense deleted successfully"}
    )