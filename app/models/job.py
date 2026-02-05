from pydantic import BaseModel, Field
from typing import Optional
from time import time

class JobCreate(BaseModel):
    jobType: str
    payload: dict
    priority: int = 5
    maxRetries: int = 3

class Job(BaseModel):
    jobId: str
    jobType: str
    payload: dict

    priority: int = 5
    maxRetries: int = 3
    attempts: int = 0

    status: str = "QUEUED"
    error: Optional[str] = None

    lockedBy: Optional[str] = None
    lockedAt: Optional[float] = None

    createdAt: float = Field(default_factory=time)
    updatedAt: float = Field(default_factory=time)
