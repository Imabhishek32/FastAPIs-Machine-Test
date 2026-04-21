
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, datetime
from dependencies import get_db, get_current_user 

router = APIRouter(prefix="/clients", tags=["Client"])

@router.post("/")
def create_client(
    client: schemas.ClientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    db_client = models.Client(
        client_name=client.client_name,
        created_by=user.id
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return {
        "id": db_client.id,
        "client_name": db_client.client_name,
        "created_at": db_client.created_at,
        "created_by": user.name
    }


@router.get("/")
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()

    result = []
    for c in clients:
        user = db.query(models.User).filter(models.User.id == c.created_by).first()

        result.append({
            "id": c.id,
            "client_name": c.client_name,
            "created_at": c.created_at,
            "created_by": user.name if user else None
        })

    return result

@router.get("/{id}")
def get_client(id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    user = db.query(models.User).filter(models.User.id == client.created_by).first()

    projects = []
    for p in client.projects:
        projects.append({
            "id": p.id,
            "project_name": p.project_name
        })

    return {
        "id": client.id,
        "client_name": client.client_name,
        "created_at": client.created_at,
        "created_by": user.name if user else None,
        "projects": projects
    }

@router.put("/{id}")
def update_client(
    id: int,
    updated_client: schemas.ClientCreate,
    db: Session = Depends(get_db)
):
    client = db.query(models.Client).filter(models.Client.id == id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.client_name = updated_client.client_name

    db.commit()
    db.refresh(client)

    return {
        "id": client.id,
        "client_name": client.client_name,
        "created_at": client.created_at
    }

@router.delete("/{id}", status_code=204)
def delete_client(id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.id == id).first()

    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()