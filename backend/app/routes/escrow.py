from fastapi import APIRouter, HTTPException, Depends

from .schema import MilestoneAction
from backend.app.services.escrow import fund_milestone, release_milestone, get_milestones
from backend.app.utils.jwt_auth import authenticate_user

router = APIRouter(prefix="/escrow", dependencies=[Depends(authenticate_user)])

@router.get("/milestones/{invoice_id}")
def api_get_milestones(invoice_id: int):
    try:
        milestones = get_milestones(invoice_id)
        return {"milestones": milestones}
    except Exception as e:
        raise HTTPException(400, str(e))

@router.post("/fund")
def api_fund(data: MilestoneAction):
    try:
        receipt = fund_milestone(data.invoice_id, data.index)
        return {"status": "funded", "tx_hash": receipt.transactionHash.hex()}
    except Exception as e:
        raise HTTPException(400, str(e))
    
@router.post("/release")
def api_release(data: MilestoneAction):
    try:
        receipt = release_milestone(data.invoice_id, data.index)
        return {"status": "released", "txn_hash": receipt.transactionHash.hex()}
    except Exception as e:
        raise HTTPException(400, str(e))
    
