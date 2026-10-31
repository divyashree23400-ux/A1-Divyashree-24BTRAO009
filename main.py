from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from models import Task, TaskCreate, TaskUpdate

app = FastAPI(
    title="Student Task API",
    description="A simple in-memory REST API for managing student tasks.",
)


def error_response(message: str, status_code: int) -> JSONResponse:
    """Return every API error in the same JSON shape."""
    return JSONResponse(
        status_code=status_code,
        content={"error": message, "status_code": status_code},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return error_response(str(exc.detail), exc.status_code)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    for err in exc.errors():
        location = err.get("loc", ())
        error_type = err.get("type", "")
        if "title" in location and error_type in {
            "string_too_short",
            "missing",
            "string_type",
            "value_error",
        }:
            return error_response("Title must not be empty", 400)

    if exc.errors():
        message = exc.errors()[0].get("msg", "Invalid request")
    else:
        message = "Invalid request"
    return error_response(message, 400)

# In-memory store: task id -> Task
tasks: dict[int, Task] = {}
next_id: int = 1


def reset_store() -> None:
    """Clear stored tasks. Used by tests to start from a clean state."""
    global next_id
    tasks.clear()
    next_id = 1


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Student Task API is running"}


@app.get("/tasks", response_model=list[Task])
def list_tasks() -> list[Task]:
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate) -> Task:
    global next_id
    task = Task(id=next_id, **payload.model_dump())
    tasks[next_id] = task
    next_id += 1
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    updates = payload.model_dump(exclude_unset=True)
    updated = task.model_copy(update=updates)
    tasks[task_id] = updated
    return updated


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
