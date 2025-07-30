from sqlalchemy.orm import Session

from . import models, schemas

# PUBLIC_INTERFACE
def get_todo(db: Session, todo_id: int):
    """Retrieve a todo by its ID."""
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

# PUBLIC_INTERFACE
def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of todos."""
    return db.query(models.Todo).offset(skip).limit(limit).all()

# PUBLIC_INTERFACE
def create_todo(db: Session, todo: schemas.TodoCreate):
    """Create a new todo."""
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# PUBLIC_INTERFACE
def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    """Update an existing todo."""
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None
    if todo.title is not None:
        db_todo.title = todo.title
    if todo.description is not None:
        db_todo.description = todo.description
    if todo.completed is not None:
        db_todo.completed = todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo

# PUBLIC_INTERFACE
def delete_todo(db: Session, todo_id: int):
    """Delete a todo."""
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None
    db.delete(db_todo)
    db.commit()
    return db_todo

# PUBLIC_INTERFACE
def set_complete_status(db: Session, todo_id: int, complete: bool):
    """Set completion status for a todo."""
    db_todo = get_todo(db, todo_id)
    if db_todo is None:
        return None
    db_todo.completed = complete
    db.commit()
    db.refresh(db_todo)
    return db_todo
