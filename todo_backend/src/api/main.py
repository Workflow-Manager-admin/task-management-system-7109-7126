from typing import List

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from . import models, schemas, crud, database

# Load .env if present
load_dotenv()

# FastAPI app setup with OpenAPI metadata and tags
app = FastAPI(
    title="Todo Backend API",
    description="RESTful API for CRUD operations on todos with persistent storage.",
    version="1.0.0",
    openapi_tags=[
        {"name": "Todos", "description": "Operations on todo items"},
        {"name": "Health", "description": "Health check endpoint"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure tables exist
models.Base.metadata.create_all(bind=database.engine)

@app.get("/", tags=["Health"])
def health_check():
    """Check backend health for liveness/readiness."""
    return {"message": "Healthy"}

# PUBLIC_INTERFACE
@app.get("/todos", response_model=List[schemas.TodoOut], summary="List all todos", tags=["Todos"])
def list_todos(skip: int = 0, limit: int = 100, db=Depends(database.get_db)):
    """
    Retrieve a list of all todos.

    - **skip**: Number of records to skip for pagination
    - **limit**: Maximum number of records returned
    """
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

# PUBLIC_INTERFACE
@app.post("/todos", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED, summary="Create a new todo", tags=["Todos"])
def create_todo(todo: schemas.TodoCreate, db=Depends(database.get_db)):
    """
    Create a new todo item.

    - **title**: Title of the todo
    - **description**: Optional description
    """
    return crud.create_todo(db, todo)

# PUBLIC_INTERFACE
@app.get("/todos/{todo_id}", response_model=schemas.TodoOut, summary="Get todo by ID", tags=["Todos"])
def get_todo(todo_id: int, db=Depends(database.get_db)):
    """
    Retrieve a todo by its ID.

    - **todo_id**: ID of the todo
    """
    db_todo = crud.get_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# PUBLIC_INTERFACE
@app.put("/todos/{todo_id}", response_model=schemas.TodoOut, summary="Update todo by ID", tags=["Todos"])
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db=Depends(database.get_db)):
    """
    Update fields of a todo.

    - **todo_id**: ID of the todo to update
    """
    db_todo = crud.update_todo(db, todo_id, todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# PUBLIC_INTERFACE
@app.patch("/todos/{todo_id}/complete", response_model=schemas.TodoOut, summary="Mark as complete/incomplete", tags=["Todos"])
def set_todo_complete_status(todo_id: int, complete: bool, db=Depends(database.get_db)):
    """
    Set the completion status of a todo.

    - **todo_id**: ID of the todo
    - **complete**: true/false
    """
    db_todo = crud.set_complete_status(db, todo_id, complete)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

# PUBLIC_INTERFACE
@app.delete("/todos/{todo_id}", response_model=schemas.TodoOut, summary="Delete todo by ID", tags=["Todos"])
def delete_todo(todo_id: int, db=Depends(database.get_db)):
    """
    Delete a todo by its ID.

    - **todo_id**: ID of the todo
    """
    db_todo = crud.delete_todo(db, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo
