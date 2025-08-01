# backend/app/wrappers.py

import os
import requests
from typing import Any, Dict

API_URL = os.getenv("API_URL", "http://localhost:8000")

def create_invoice_tool(client:str, freelancer: str, milestone_amounts: list[int]) -> Dict[str, Any]:
    """
    Deploys a new escrow + invoice on-chain and records it in the DB.
    """
    resp = requests.post(
        f"{API_URL}/invoice",
        json={
            "client": client,
            "freelancer": freelancer,
            "milestone_amounts": milestone_amounts
        },
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()

def fund_milestone_tool(invoice_id: int, milestone_index: int) -> Dict[str, Any]:
    """
    Funds a specific milestone (on-chain) for the given invoice.
    """
    # We pass invoice_id as a query param so the handler can verify scope if needed
    resp = requests.post(
        f"{API_URL}/escrow/fund",
        json={"invoice_id": invoice_id, "index": milestone_index},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()

def release_milestone_tool(invoice_id: int, milestone_index: int) -> Dict[str, Any]:
    """
    Releases funds for a specific milestone (on-chain) of the given invoice.
    """
    resp = requests.post(
        f"{API_URL}/escrow/release",
        json={"invoice_id": invoice_id, "index": milestone_index},
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()

def get_invoice_tool(invoice_id: int) -> Dict[str, Any]:
    """
    Retrieves complete information of invoice status from DB
    """
    resp = requests.get(
        f"{API_URL}/invoice/{invoice_id}",
        timeout=10
    )
    resp.raise_for_status()
    return resp.json()