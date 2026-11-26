from fastapi import FastAPI
from loguru import logger
from routes.auth import auth_router
from routes.Task import Task_route
from db.database import init_db
from model.user import User
from model.task import CreateTask
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    try:
        await init_db()
    except Exception as exc:
        # La base peut être momentanément indisponible (veille Neon, réseau).
        # On laisse l'API démarrer pour ne pas faire échouer le health check.
        logger.warning("Initialisation de la base échouée au démarrage : {}", exc)


app.include_router(auth_router)
app.include_router(Task_route)