import time
import uuid
from app.services.job_service import JobService
from app.database.mongodb import db, worker_collection

WORKER_ID = str(uuid.uuid4())

def process_job(job):
    # Simulated job execution
    print(f"Worker {WORKER_ID} processing job {job['jobId']}")
    time.sleep(2)
    if job["jobType"] == "fail":
        raise Exception("Simulated failure")

def heartbeat(worker_id: str):
    worker_collection.update_one(
        {"workerId": worker_id},
        {
            "$set": {
                "lastSeen": time.time()
            }
        },
        upsert=True
    )
while True:
    heartbeat(WORKER_ID)

    job = JobService.fetch_next_job(WORKER_ID)

    if not job:
        time.sleep(2)
        continue

    try:
        process_job(job)
        JobService.mark_success(job["jobId"])
    except Exception as e:
        JobService.mark_failure(
            job["jobId"],
            str(e),
            job["attempts"],
            job["maxRetries"]
        )
