from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
# from app.stores.models import 