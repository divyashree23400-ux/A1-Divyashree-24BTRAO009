from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """Fields required to create a new student task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    student_name: str = Field(..., min_length=1, max_length=100)
    completed: bool = False


class TaskUpdate(BaseModel):
    """Optional fields for updating an existing task."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    student_name: str | None = Field(default=None, min_length=1, max_length=100)
    completed: bool | None = None


class Task(TaskCreate):
    """A stored task, including its generated id."""

    id: int
