# from fastapi import FastAPI
from database import Base, engine
Base.metadata.create_all(bind=engine)

from fastapi import FastAPI
from routers import user, client, project, auth
from database import Base, engine
import models  

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(client.router)
app.include_router(project.router)

@app.get("/")
def home():
    return {"Message": "Hello Welcome to my Nimap Infotech Task This APIs create by Abhishek Chaurasiya"}