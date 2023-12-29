"""
path: app/routers/main.py

This file contains the main router for the application.
"""

from typing import List

from fastapi import APIRouter, Request, BackgroundTasks, File, UploadFile, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request

from app.sheet import SheetsClient
from app.config import settings
from app.process import process_file

import os


router = APIRouter()
# template directory is in the root directory
# router.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

# Dependency to get the session
def get_session(request: Request):
    """
    Returns the session from the request
    """
    return request.session

@router.get("/login")
async def login_form(request: Request):
    """
    Renders the login form
    """
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def authenticate(
    username: str = Form(...),
    password: str = Form(...),
    session: dict = Depends(get_session)):
    """
    Authenticates the user and stores it in the session
    """
    if (username == settings.SUPPER_USER and password == settings.SUPPER_USER_PASSWORD) or (username == settings.USERNAME and password == settings.PASSWORD):
        session["user"] = username  # Store the logged-in user in the session
        return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

@router.get("/", response_class=HTMLResponse)
async def upload_form(request: Request, session: dict = Depends(get_session)):
    """
    Renders the upload form
    """
    if "user" in session:
        return templates.TemplateResponse("index.html", {"request": request})
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.post("/")
async def upload_file(background_tasks: BackgroundTasks,
                      files: List[UploadFile] = File(...),
                      session: dict = Depends(get_session)):
    """
    Uploads a file and create a background task to process the file.
    """
    if "user" in session:   
        sheets_client = SheetsClient(credentials_file_path=settings.CREDENTIALS_FILE_PATH)
        for file in files:
            background_tasks.add_task(process_file, file, sheets_client)
        message = f"{len(files)} invoices uploaded successfully and will be processed in the background."
        return {"message": message}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please login to upload files")
