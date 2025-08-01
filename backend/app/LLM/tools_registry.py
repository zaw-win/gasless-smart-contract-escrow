from langchain.tools import Tool
from ..routes.schema import (
    MilestoneAction,
    InvoiceCreate,
    InvoiceGet
)
from .wrappers import (
    fund_milestone_tool,
    release_milestone_tool,
    create_invoice_tool,
    get_invoice_tool
)

tools = [
    Tool.from_function(
        func = create_invoice_tool,
        name = "create_invoice",
        description="Deploys an escrow contract and creates a new invoice for a freelancer by a client",
        args_schema=InvoiceCreate
    ),
    Tool.from_function(
        func = fund_milestone_tool,
        name = "fund_milestone",
        description = "Funds a specific milestone of an existing invoice on-chain.",
        args_schema=MilestoneAction
    ),
    Tool.from_function(
        func = release_milestone_tool,
        name = "release_milestone",
        description = "Releases funds for a specific milestone of an invoice on-chain.",
        args_schema=MilestoneAction
    ),
    Tool.from_function(
        func = get_invoice_tool,
        name = "get_invoice",
        description="Retrieves all the components of a specific invoice.",
        args_schema=InvoiceGet
    )
]