from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, crud, auth, database

router = APIRouter()

# User Endpoints
@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    users = crud.get_all_users(db)
    return users

# Task Endpoints
@router.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return crud.create_task(db, task, user_id=current_user.id)

@router.get("/tasks", response_model=list[schemas.TaskOut])
def list_tasks(status: str | None = None, current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if status:
        return crud.get_tasks_by_status(db, user_id=current_user.id, status=status)
    return crud.get_tasks(db, user_id=current_user.id)

@router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    task = crud.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    task = crud.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task_id, current_user.id)
    return {"message": "Tarea borrada"}

@router.put("/tasks/{task_id}", response_model=dict)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    task = crud.update_task(db, task_id, task_update, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Tarea actualizada"}

@router.patch("/tasks/{task_id}/complete", response_model=dict)
def complete_task(task_id: int, db: Session = Depends(database.get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    task = crud.get_task_by_id(db, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.status = "completed"
    db.commit()
    db.refresh(task)
    return {"message": "Tarea marcada como completada"}

# Admin Endpoints
@router.get("/admin/users", response_model=list[schemas.UserOut])
def get_all_users(current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_all_users(db)

@router.get("/admin/tasks", response_model=list[schemas.TaskOut])
def get_all_tasks(current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    return crud.get_all_tasks(db)

@router.delete("/admin/users/{user_id}", response_model=dict)
def delete_user(user_id: int, current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    crud.delete_user(db, user_id)
    return {"message": "Usuario eliminado"}

@router.patch("/admin/users/{user_id}/make-admin", response_model=dict)
def make_user_admin(user_id: int, current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    db.commit()
    db.refresh(user)
    return {"message": "Usuario ahora es administrador"}

@router.get("/admin/stats", response_model=dict)
def get_dashboard_stats(current_user=Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")

    total_tasks = crud.get_total_tasks(db)
    completed_tasks = crud.get_tasks_by_status_count(db, status="completed")
    pending_tasks = crud.get_tasks_by_status_count(db, status="pending")
    tasks_by_user = crud.get_tasks_count_by_user(db)

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "tasks_by_user": tasks_by_user
    }

