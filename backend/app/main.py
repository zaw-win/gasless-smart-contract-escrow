# backend/app/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.app.routes.escrow import router as escrow_router 
from .routes.invoice import router as invoice_router
from .routes.users import router as users_router
# from .routes.chat import router as chat_router
from backend.app.database.utils import execute_sql
from backend.app.database.ddl import *
# from backend.app.services.event_listener import run_event_listener
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_):
    # order matters
    execute_sql(create_users_tbl) 
    execute_sql(create_invoices_tbl)
    execute_sql(create_milestones_tbl)
    
    # create_milestones_table()
    # create_invoice_table()
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:3000"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers= ["*"]
)
@app.get("/")
def root():
    return {"message": "Backend is running"}

app.include_router(escrow_router)
app.include_router(invoice_router)
app.include_router(users_router)
# app.include_router(chat_router)