# from fastapi import APIRouter, HTTPException
# from ..LLM.agent import agent
# from .schema import ChatRequest, ChatResponse

# router = APIRouter()

# @router.post("/chat")
# def chat(req: ChatRequest):
#     try:
#         # Use output_keys to specify what we want returned
#         reply = agent.invoke(
#             {"messages": [{"role": "user", "content": req.message}]},
#         )            
#         return reply["messages"][-1].content
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))