from pydantic import BaseModel, Field

class MilestoneAction(BaseModel):
    invoice_id: int = Field(..., description="The numeric ID of the invoice")
    index: int = Field(..., description="Zero-based index of the milestone to fund")

class InvoiceCreate(BaseModel):
    client_email: str = Field(..., description = "The email address of the client")
    freelancer_email: str =  Field(..., description ="The email address  of the freelancer")
    milestone_amounts: list[int] = Field(..., min_items=1, description=
                                         "List of milestone amounts in USDC"
                                         )

class InvoiceOut(BaseModel):
    invoice_id: int = Field(..., description="The numeric ID of the invoice")
    escrow: str = Field(..., description="The blockchain address of the escrow")
    client_email: str = Field(..., description="The email address  of the client")
    freelancer_email: str = Field(..., description="The email address  of the freelancer")
    milestones: list[dict] = Field(..., description="The comprehensive list of milestones and its attributes")

class InvoiceGet(BaseModel):
    invoice_id: int = Field(..., description="The numeric ID of the invoice")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: dict