from pydantic import BaseModel, Field, field_validator


def require_non_blank_title(value: str | None) -> str | None:
    """Reject missing text after trimming spaces; keep None for omitted updates."""
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        raise ValueError("Title must not be empty")
    return stripped


class TaskCreate(BaseModel):
    """Fields required to create a new student task."""

    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    student_name: str = Field(..., min_length=1, max_length=100)
    completed: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        return require_non_blank_title(value)


class TaskUpdate(BaseModel):
    """Optional fields for updating an existing task."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    student_name: str | None = Field(default=None, min_length=1, max_length=100)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str | None) -> str | None:
        return require_non_blank_title(value)


class Task(TaskCreate):
    """A stored task, including its generated id."""

    id: int
