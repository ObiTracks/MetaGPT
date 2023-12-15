# Command to run server: uvicorn app.main:app --reload
import os
from typing import Union
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger as fastapi_logger
import uvicorn
from contextlib import asynccontextmanager
import socketio
from fastapi_socketio import SocketManager
import logging
from .database import connect_to_mongo, close_mongo_connection
from .core import config
from jose import JWTError, jwt
from .models import Webhook, Branch, Commit, Action, Message, Question, ConsultScaffold, Task, ChatRequest, Conversation, AISession, Repository, RateLimit, User
# If metagpt is located in a subfolder, uncomment this with the correct path
# to add it to the Python path
# import sys
# sys.path.append('/path/to/metagpt')  # Replace with the actual path

# main.py
from pydantic import BaseModel
import asyncio

from metagpt.roles import Architect, Engineer, ProductManager, ProjectManager, QaEngineer
from metagpt.team import Team

app = FastAPI()

# Define request model
class StartupRequest(BaseModel):
    idea: str
    investment: float = 3.0
    n_round: int = 5
    code_review: bool = False
    run_tests: bool = False
    implement: bool = True

async def startup(idea: str, investment: float, n_round: int, code_review: bool, run_tests: bool, implement: bool):
    company = Team()
    company.hire([ProductManager(), Architect(), ProjectManager()])

    if implement or code_review:
        company.hire([Engineer(n_borg=5, use_code_review=code_review)])

    if run_tests:
        company.hire([QaEngineer()])

    company.invest(investment)
    company.start_project(idea)
    await company.run(n_round=n_round)

@app.post("/generate")
async def generate(request: StartupRequest):
    try:
        await startup(
            request.idea, request.investment, request.n_round, 
            request.code_review, request.run_tests, request.implement
        )
        return {"message": "Startup process initiated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
