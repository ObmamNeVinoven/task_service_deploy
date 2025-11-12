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

## ☁️ 1. Cloud Deployment (Render + MongoDB Atlas)

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

---

## 🖥 2. Local Development (Docker Compose)

This mode is used for local development and testing, including interaction with other microservices (`pet-service` and `notification-service`).

This configuration runs a **fully High-Availability (HA)** system of 11 containers:
* 3 x MongoDB Replica Set nodes 
* 1 x `mongo-setup` 
* 2 x `task-service` 
* 2 x `pet-service` 
* 2 x `notification-service` 
* 1 x `nginx-lb` (Load Balancer)

### Setup Instructions

**Prerequisites:**
* Docker
* Docker Compose

**How to Run:**

1.  Ensure all 3 service folders (`task-service`, `pet-service`, `notification-service`) and the 2 config files (`docker-compose.yml`, `nginx.conf`) are in the same root directory.
2.  Run the following command in your terminal:

    ```bash
    docker-compose up --build
    ```

**Local Endpoints:**
* **Task Service:** `http://localhost:8081`
* **Pet Service:** `http://localhost:8082`
* **Notification Service:** `http://localhost:8083`

---

## 👤 Authors

* **Name:** Ellen Seitkassimova, Bauyrzhan Yerzhanov, Eduard Shilke
* **Course:** Software Architecture
