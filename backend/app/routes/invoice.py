from fastapi import APIRouter, HTTPException, Depends
from ..services.escrow import create_escrow
from .schema import InvoiceCreate, InvoiceOut
from ..database.invoices import get_invoice_info_with_milestones
from ..database.users import does_user_exist
from ..utils.jwt_auth import authenticate_user

router = APIRouter(
    prefix="/invoice",
    dependencies=[Depends(authenticate_user)]
    )

@router.post("/", status_code=201)
def create_invoice(data: InvoiceCreate):
    if not does_user_exist(data.client_email):
        raise HTTPException(401, f"{data.client_email} does not exist.")
    
    if not does_user_exist(data.freelancer_email):
        raise HTTPException(401, f"{data.freelancer_email} does not exist.")
    # this function will deploy ESCROW Contract on Base Sepolia Chain
    return create_escrow(
        client_email=data.client_email, 
        freelancer_email=data.freelancer_email, 
        milestone_amounts=data.milestone_amounts
        )

@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int):
    try:
        return get_invoice_info_with_milestones(invoice_id)
    except Exception as e:
        print(e)
        raise HTTPException(404, "Invoice not found")