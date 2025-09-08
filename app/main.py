from fastapi import FastAPI
from app.routes.AI_tutor import router

app= FastAPI()
app.include_router(router)