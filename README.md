# 🚀 Task Service (Microservice)

This is a `task-service`, a FastAPI microservice developed for the Software Architecture course. It manages user authentication and assignments.

This service uses **MongoDB** for data persistence and follows **Clean Architecture** principles, separating logic into Domain, Usecase, Adapters, and Infrastructure layers.

---

## 🛠 Tech Stack

* **Framework:** FastAPI
* **Database:** MongoDB (local) / MongoDB Atlas (cloud)
* **Containerization:** Docker / Docker Compose
* **Deployment Platform:** Render
* **Validation:** Pydantic
* **Authentication:** JWT (python-jose) & Passlib

---

## ☁️ Cloud Deployment (Render + MongoDB Atlas)

This is the primary production deployment required by the assignment.

**Live Endpoints:**
* **Live URL:** `https://task-service-deploy.onrender.com`
* **Swagger UI (Docs):** `https://task-service-deploy.onrender.com/docs`
* **DB Health Check:** `https://task-service-deploy.onrender.com/health/db`

### Deployment Setup

The service is deployed on **Render** using Docker. It connects to a **MongoDB Atlas** `M0` free-tier cluster.

**Environment Variables configured in Render:**
* `MONGO_URI`: [Secret] The connection string for the MongoDB Atlas cluster.
* `DB_NAME`: The name of the database (e.g., `assignmentdb`).
* `JWT_SECRET`: [Secret] A secret key for signing JWT tokens.
* `PET_SERVICE_URL`: (Dummy) `http://dummy.com`
* `NOTIFICATION_SERVICE_URL`: (Dummy) `http://dummy.com`


## 👤 Authors

* **Name:** Ellen Seitkassimova, Bauyrzhan Yerzhanov, Eduard Shilke
* **Course:** Software Architecture
