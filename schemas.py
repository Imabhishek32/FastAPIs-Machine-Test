from pydantic import BaseModel, EmailStr
from typing import List
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    client_name: str


class ClientResponse(BaseModel):
    id: int
    client_name: str
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectCreate(BaseModel):
    project_name: str
    client_id: int
    users: List[int]


class ProjectOut(BaseModel):
    id: int
    project_name: str
    client: ClientResponse 
    users: List[UserOut]

    class Config:
        from_attributes = True