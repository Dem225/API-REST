from fastapi import FastAPI
from routes.auth import auth_router
from routes.Task import Task_route
app = FastAPI()

app.include_router(auth_router)
app.include_router(Task_route)