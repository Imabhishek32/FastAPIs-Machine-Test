from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, datetime
from dependencies import get_db, get_current_user

router = APIRouter(prefix="/project")

router = APIRouter(prefix="/project", tags=["Project"])
prefix="/project"
@router.get("/{id}")


@router.post("/")
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):

    client = db.query(models.Client).filter(models.Client.id == project.client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db_project = models.Project(
        project_name=project.project_name,
        client_id=project.client_id
    )

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


@router.get("/")
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()



@router.get("/{id}")
def get_project(id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    return project