from fastapi import APIRouter
from app.models.job import Job, JobCreate
from app.services.job_service import JobService
router = APIRouter(prefix="/jobs", tags=["Jobs"])
from typing import Optional

@router.get("/")
def get_jobs(status: Optional[str] = None):
    return JobService.list_jobs_filtered(status)


@router.post("/")
def submit_job(job: JobCreate):
    return JobService.create_job(job)

@router.get("/stats")
def job_stats():
    return JobService.get_stats()

@router.post("/requeue-stuck")
def requeue_stuck():
    count = JobService.requeue_stuck_jobs()
    return {"requeued": count}

@router.get("/workers")
def get_workers():
    return JobService.list_workers()
