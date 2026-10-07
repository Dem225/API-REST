from fastapi import FastAPI
from routes.auth import auth_router
from routes.Task import Task_route
from db.database import init_db
from model.user import User
from model.task import CreateTask
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()


app.include_router(auth_router)
app.include_router(Task_route)