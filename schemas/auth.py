
from pydantic import BaseModel, EmailStr , Field 

class UserCreate(BaseModel):
        nom: str =Field(min_length=3 , max_length=50)
        prenom: str =Field(min_length=3 , max_length=50)
        email : EmailStr 
        password: str =Field(min_length=8)

class Conexions(BaseModel):
        email:EmailStr
        password:str
        


