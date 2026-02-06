# AegisQueue
### A Fault-Tolerant Distributed Job Queue & Scheduler (Backend)

AegisQueue is a backend-focused distributed job queue designed to reliably execute background tasks using multiple workers with strong guarantees around correctness, concurrency safety, and fault recovery.

The system emphasizes **atomic job claiming**, **state-driven execution**, and **observability**, making it suitable for learning and demonstrating real-world backend and distributed systems concepts.

---

## ✨ Key Features

- **Distributed Workers**
  - Multiple workers safely compete for jobs without duplicate execution
  - Atomic job claiming using MongoDB `find_one_and_update`

- **State-Driven Job Lifecycle**
  - Deterministic transitions:  
    `QUEUED → RUNNING → SUCCESS / FAILED`
  - Retry support with max-retry enforcement
  - Failure persistence for debugging and observability

- **Priority-Based Scheduling**
  - Jobs are scheduled using priority levels
  - FIFO ordering within the same priority class

- **Worker Heartbeats & Liveness Detection**
  - Workers periodically report heartbeats
  - System detects active vs dead workers in real time

- **Fault Recovery**
  - Automatically detects stuck jobs (e.g. worker crash mid-execution)
  - Safely requeues jobs for retry without duplication

- **Monitoring & Observability APIs**
  - Job filtering by status
  - System-wide job statistics
  - Worker status inspection
  - Administrative recovery endpoints

---

## 🏗️ System Architecture

The diagram below illustrates the backend architecture of **AegisQueue**, highlighting the separation between the control plane, execution workers, and the database used for coordination and fault tolerance.

![AegisQueue Architecture](./architecture.png)

## 🧠 System Design Overview

- **Concurrency Safety:**  
  Achieved using atomic MongoDB operations instead of in-memory locks.

- **At-Least-Once Execution:**  
  Jobs are retried on failure up to a configurable limit.

- **Crash Resilience:**  
  Worker crashes do not corrupt job state; stuck jobs are recoverable.

- **Backend-First Architecture:**  
  No frontend assumptions — APIs are dashboard-ready and production-oriented.

---

## 🛠 Tech Stack

- **Backend Framework:** FastAPI (Python)
- **Database:** MongoDB
- **Database Driver:** PyMongo
- **Architecture:** REST APIs + Distributed Workers

---

## 📡 API Endpoints (Core)

| Method | Endpoint | Description |
|------|--------|-------------|
| POST | `/jobs` | Submit a new job |
| GET | `/jobs` | List jobs (optional status filter) |
| GET | `/jobs/stats` | System-wide job metrics |
| GET | `/jobs/workers` | Worker heartbeat & liveness info |
| POST | `/jobs/requeue-stuck` | Requeue stuck jobs |

---

## ⚙️ Running the Backend

### 1. Clone the repository
```bash
git clone https://github.com/spexcher/distributed-job-queue.git
cd distributed-job-queue
```
### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Start the API server
```bash
uvicorn app.main:app --reload
```
### 5. Start one or more workers
```bash
python worker.py
```

## 🔗 Links

- **Live Demo:** https://spexcher.vercel.app  
- **GitHub:** https://github.com/spexcher  
- **LinkedIn:** https://linkedin.com/in/gourabmodak  
- **Codeforces:** https://codeforces.com/profile/spexcher  
- **CLIST:** https://clist.by/coder/spexcher  
- **Email:** gourabmodak28092003@gmail.com


---

## The frontend is still in the building (job-queue-dashboard)
