from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends
import os
from dotenv import load_dotenv
load_dotenv()
URL=os.getenv("SQLALCHEMY_DATABASE_URL_URI")

# DEF ENGINE

print(URL)

engine=create_engine("URL:", URL)



#DEF OF SESSION
SessionLocal= sessionmaker(autoflush=False , autocommit=False , bind=engine)



# DEF BASE AN OBJECT TO USER


Base= declarative_base()




#DEPENDENCY

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

#DEPENDANCY ANNOTATED

bd_dependency = Annotated[Session,Depends(get_db)]


