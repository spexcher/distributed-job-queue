from app.database.mongodb import job_collection
from time import time
from pymongo import ReturnDocument
from app.models.job import Job
from app.models.job import JobCreate
from uuid import uuid4
from app.database.mongodb import worker_collection
class JobService:
    @staticmethod
    def get_stats():
        return {
            "total": job_collection.count_documents({}),
            "queued": job_collection.count_documents({"status": "QUEUED"}),
            "running": job_collection.count_documents({"status": "RUNNING"}),
            "success": job_collection.count_documents({"status": "SUCCESS"}),
            "failed": job_collection.count_documents({"status": "FAILED"})
        }

    @staticmethod
    def list_jobs_filtered(status: str | None = None, limit: int = 50):
        query = {}
        if status:
            query["status"] = status

        jobs = (
            job_collection
            .find(query, {"_id": 0})
            .sort("createdAt", -1)
            .limit(limit)
        )
        return list(jobs)
    
    @staticmethod
    def requeue_stuck_jobs(timeout_seconds: int = 30):
        cutoff = time() - timeout_seconds

        result = job_collection.update_many(
            {
                "status": "RUNNING",
                "lockedAt": {"$lt": cutoff}
            },
            {
                "$set": {
                    "status": "QUEUED",
                    "lockedBy": None,
                    "lockedAt": None,
                    "updatedAt": time()
                }
            }
        )
        return result.modified_count

    @staticmethod
    def create_job(job: JobCreate):
        job_dict = job.dict()
        job_dict.update({
            "jobId": str(uuid4()),
            "status": "QUEUED",
            "attempts": 0,
            "error": None,
            "lockedBy": None,
            "lockedAt": None,
            "createdAt": time(),
            "updatedAt": time()
        })

        job_collection.insert_one(job_dict)
        job_dict.pop("_id", None)   # 🔥 CRITICAL LINE

        return job_dict


    @staticmethod
    def list_jobs(limit: int = 50):
        jobs = job_collection.find({}, {"_id": 0}).sort("createdAt", -1).limit(limit)
        return list(jobs)

    @staticmethod
    def fetch_next_job(worker_id: str):
        return job_collection.find_one_and_update(
            {"status": "QUEUED"},
            {
                "$set": {
                    "status": "RUNNING",
                    "lockedBy": worker_id,
                    "lockedAt": time(),
                    "updatedAt": time()
                },
                "$inc": {"attempts": 1}
            },
            sort=[("priority", 1), ("createdAt", 1)],
            return_document=ReturnDocument.AFTER   # 🔥 THIS LINE
    )


    @staticmethod
    def mark_success(job_id: str):
        job_collection.update_one(
            {"jobId": job_id},
            {
                "$set": {
                    "status": "SUCCESS",
                    "error": None,
                    "updatedAt": time()
                }
            }
        )

    @staticmethod
    def mark_failure(job_id: str, error: str, attempts: int, max_retries: int):
        status = "FAILED" if attempts >= max_retries else "QUEUED"
        job_collection.update_one(
            {"jobId": job_id},
            {
                "$set": {
                    "status": status,
                    "error": error,
                    "updatedAt": time()
                }
            }
        )
        from app.database.mongodb import worker_collection

    @staticmethod
    def list_workers(timeout_seconds: int = 10):
        now = time()
        workers = list(worker_collection.find({}, {"_id": 0}))

        for w in workers:
            w["status"] = (
                "ALIVE" if now - w["lastSeen"] <= timeout_seconds else "DEAD"
            )

        return workers

