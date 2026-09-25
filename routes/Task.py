
from  fastapi  import APIRouter , Path
from db.database import db_dependency
from schemas.Task import  CreateTaskValide
from services.Task import TaskService
from services.dependance import curent_user_dependancy
Task_route=APIRouter(prefix="/Tasks", tags=["Tasks"])




@Task_route.get("/all")
async def consulter_all( db: db_dependency, current_user: curent_user_dependancy):
    service = TaskService(db)
    return await service.get_all_task(current_user.id)

@Task_route.get("/{id}")
async def consulter_one( db:db_dependency, current_user: curent_user_dependancy , id :int=Path(gt=0)):
    service=TaskService(db)
    return  await  service.get_one_task(current_user.id , id)


@Task_route.get("/filter/{status}")
async def filterer( db:db_dependency, current_user: curent_user_dependancy , status:bool=Path()):
    service = TaskService(db)
    return await service.task_filter(current_user.id ,status )

@Task_route.post("/ajouter_tache")
async def ajoutes(body:CreateTaskValide , db:db_dependency, current_user: curent_user_dependancy):
    service= TaskService(db)
    return await service.Ajouter_Task(body , current_user.id)

@Task_route.put("/Modifier/{id}")
async def modifier( id : int , body:CreateTaskValide , db:db_dependency, current_user: curent_user_dependancy):
    service=TaskService(db)
    
    return await service.update_all_task(current_user.id, id , body)


@Task_route.delete("/suppimer_tache/{id}")
async def supprimer(db:db_dependency, current_user: curent_user_dependancy,id : int = Path(gt=0) ):
    service=TaskService(db)
    
    return await service.delete_task(current_user.id,id)



