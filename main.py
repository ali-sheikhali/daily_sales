from fastapi import FastAPI, Depends, Response,Request
from contextlib import asynccontextmanager
from app.users.routes import router as users_router
from app.stores.routes import router as stores_router
from app.store_manager.routes import router as stores_manager_router
from app.sales.routes import router as sales_router
from app.expenses.routes import router as expenses_router
from app.store_recipients.routes import router as store_recipients_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app startup")
    yield
    print("app shutdown")


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(stores_router)
app.include_router(stores_manager_router)
app.include_router(sales_router)
app.include_router(expenses_router)
app.include_router(store_recipients_router)