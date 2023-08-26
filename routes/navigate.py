import jwt,os.path, time

from config.db import collection
from fastapi import APIRouter, Depends,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from config.db import permission

navigator=APIRouter()
templates=Jinja2Templates(directory="html")

@navigator.get("/",response_class=HTMLResponse)
def write_home(request : Request):
    return templates.TemplateResponse("login.html",{"request":request})