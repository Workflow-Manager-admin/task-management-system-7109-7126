from pydantic import BaseModel, Field
from typing import Optional

# PUBLIC_INTERFACE
class TodoBase(BaseModel):
    """Base fields for a Todo."""
    title: str = Field(..., description="Title of the todo")
    description: Optional[str] = Field("", description="Description of the todo")

# PUBLIC_INTERFACE
class TodoCreate(TodoBase):
    """Fields required for creating a Todo."""
    pass

# PUBLIC_INTERFACE
class TodoUpdate(BaseModel):
    """Fields for updating a Todo."""
    title: Optional[str] = Field(None, description="Title of the todo")
    description: Optional[str] = Field(None, description="Description of the todo")
    completed: Optional[bool] = Field(None, description="Completion status")

# PUBLIC_INTERFACE
class TodoOut(TodoBase):
    """Representation of a Todo returned from API."""
    id: int = Field(..., description="ID of the Todo")
    completed: bool = Field(False, description="Completion status")
    created_at: Optional[str]
    updated_at: Optional[str]
    class Config:
        orm_mode = True
