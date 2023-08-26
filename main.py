from fastapi import FastAPI
from routes.navigate import navigator
from routes.jobs import jobs
from fastapi.staticfiles import StaticFiles
import uvicorn

app=FastAPI()

app.mount("/static", StaticFiles(directory="html/static"), name="static")

app.include_router(navigator)
app.include_router(jobs)

uvicorn.run(app,host='localhost',port=8000)