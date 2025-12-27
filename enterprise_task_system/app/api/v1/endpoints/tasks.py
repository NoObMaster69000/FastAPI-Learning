# enterprise_task_system/app/api/v1/endpoints/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
from typing import List

from app import models, schemas
from app.api import deps
from app.services.task_service import task_service
from app.repositories.task_repository import task_repository

router = APIRouter()


@router.get("/", response_model=List[schemas.task.Task])
def read_tasks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_user),
) -> List[models.task.Task]:
    """
    Retrieve tasks.
    """
    tasks = task_repository.get_multi_by_owner(
        db, owner_id=current_user.id, skip=skip, limit=limit
    )
    return tasks


@router.get("/{task_id}", response_model=schemas.task.Task)
def read_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: uuid.UUID,
    current_user: models.user.User = Depends(deps.get_current_user),
) -> models.task.Task:
    """
    Get task by ID.
    """
    task = task_repository.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return task


@router.delete("/{task_id}", response_model=schemas.task.Task)
def delete_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: uuid.UUID,
    current_user: models.user.User = Depends(deps.get_current_user),
) -> models.task.Task:
    """
    Delete a task.
    """
    task = task_repository.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task = task_repository.remove(db=db, id=task_id)
    return task


@router.put("/{task_id}", response_model=schemas.task.Task)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    task_id: uuid.UUID,
    task_in: schemas.task.TaskUpdate,
    current_user: models.user.User = Depends(deps.get_current_user),
) -> models.task.Task:
    """
    Update a task.
    """
    task = task_repository.get(db=db, id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    task = task_repository.update(db=db, db_obj=task, obj_in=task_in)
    return task


@router.post("/", response_model=schemas.task.Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    task_in: schemas.task.TaskCreate,
    current_user: models.user.User = Depends(deps.get_current_user),
) -> models.task.Task:
    """
    Create new task.
    """
    task = task_service.create_task(db=db, obj_in=task_in, owner=current_user)
    return task
