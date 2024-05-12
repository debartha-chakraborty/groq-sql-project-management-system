from datetime import datetime
from pydantic import BaseModel, Field


class EmployeeSchema(BaseModel):
    name: str
    designation: str
    skills: str | None = None
    active_project_count: int = Field(default=0, description="Number of active projects assigned to the employee")


class TaskSchema(BaseModel):
    title: str
    description: str
    request_date: datetime = Field(default_factory=datetime.utcnow, description="Date and time the task was requested")
    tech: str
    ideal_skills: str | None = None


class JobSchema(BaseModel):
    emp_id: int
    task_id: int
    assignment_date: datetime = Field(default_factory=TaskSchema.request_date.default_factory, description="Date and time the task was assigned")
    estimated_time: int | None = None
    completion_date: datetime | None = None
    status: str | None = None
