
from model.user import User
from db.database import db_dependency
from loguru import logger
from schemas.Task import CreateTaskValide
from model.task import CreateTask
from fastapi import HTTPException
from sqlalchemy import select
class TaskService :

    def __init__(self , db:db_dependency):
        self.db = db


    async  def  Ajouter_Task(sefl , Body_task:CreateTaskValide , user_id:int):

        new_task= CreateTask(
        title = Body_task.title,
        description =Body_task.description,
        priority = Body_task.priority,
        completed=Body_task.completed, 
        userId = user_id
        )

        sefl.db.add(new_task)

        await sefl.db.commit()
        await sefl.db.refresh(new_task)

        logger.info("Task ajouter ace succes ! ")

        return  new_task

    async def get_all_task(self, user_id: int):

        result = await self.db.execute(
            select(CreateTask).where(
                CreateTask.userId == user_id
            )
        )

        return result.scalars().all()

    
    async def get_one_task(self, user_Id: int , task_id : int):

        resultat= await self.db.execute(
            select(CreateTask).where(
                CreateTask.userId == user_Id ,
                CreateTask.id == task_id 
                
            )
        )

        task=resultat.scalar_one_or_none()

        if task is None :
            raise HTTPException(
                status_code=404 ,
                detail="Task introuvable "
            )

        return task



    async def update_all_task(self , user_id : int , task_id : int , body_task:CreateTaskValide):

        resultat=  await self.db.execute(
            select(CreateTask).where(
                CreateTask.userId== user_id,
                CreateTask.id == task_id
            )
        )

        task= resultat.scalar_one_or_none()
        
        if task is None :
           
            raise HTTPException(
                status_code=404 ,
                detail="Tâche introuvable ou vous n'êtes pas autorisé !"
            )  
                                                                                   
        task.title=body_task.title
        task.description= body_task.description
        task.priority= body_task.priority   
        task.completed= body_task.completed

        await self.db.commit()
        await self.db.refresh(task)
        logger.info("Task modifiée avec succès !")

        return task


    async def delete_task (self, user_id:int , task_id:int):
        
        resultat= await self.db.execute(
            select(CreateTask).where(
                CreateTask.userId== user_id ,
                CreateTask.id== task_id,
            )
        )
        task= resultat.scalar_one_or_none()
        if not task:
            raise HTTPException(status_code=404 ,detail="Task n 'exite pas ! ")
        
        await self.db.delete(task)
        await self.db.commit()
        
        return task


    async def task_filter(sel , user_id:int , status:bool):
        resultat= await sel.db.execute(
            select(CreateTask).where(
                CreateTask.userId== user_id,
                CreateTask.completed == status
            )
        )
       
        task= resultat.scalars().all()
       
        if not task :
            raise HTTPException(status_code=404 , detail="Pas de tache !")

        return task












        


