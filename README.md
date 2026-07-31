#   Real-Time Chat & Collaboration App

A production-ready, scalable real-time chat and collaboration backend built with **FastAPI**, **PostgreSQL**, **Redis**, **WebSockets**, and **Docker**. This project follows **Clean Architecture**, **Repository Pattern**, **Service Layer**, and modern backend engineering practices used in product-based companies.

Designed to demonstrate backend engineering skills required for Software Engineer roles.

---

#   Features

## Authentication

* JWT Authentication
* Access & Refresh Tokens
* Secure Password Hashing
* User Registration
* User Login
* Current User API
* Role-Based Access Control (RBAC)

## User Management

* User Profile
* Profile Update
* Online/Offline Presence

## Real-Time Messaging

* One-to-One Chat
* Group Chat
* WebSocket Communication
* Typing Indicators
* Read Receipts
* Message Pagination
* Message History
* Redis Pub/Sub Integration

## Media

* Image Upload
* File Validation
* AWS S3 Ready Structure

## Notifications

* Push Notifications
* Background Tasks

## Production Features

* Docker Support
* Docker Compose
* PostgreSQL
* Redis
* Alembic Migrations
* Structured Logging
* Global Exception Handling
* Rate Limiting
* Caching
* Health Checks
* Environment-Based Configuration
* CI/CD Ready Structure
* AWS Deployment Ready
* Nginx Reverse Proxy Ready

---

#  Tech Stack

## Backend

* FastAPI
* Python 3.12+
* SQLAlchemy 2.0
* Pydantic v2
* PostgreSQL
* Alembic
* Redis
* WebSockets
* JWT
* Passlib
* Docker

## DevOps

* Docker
* Docker Compose
* AWS EC2
* Nginx
* GitHub Actions (CI/CD Ready)

## Frontend (Planned)

* Flutter

---

#  Project Structure

```text
real-time-chat-app/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── services/
│   ├── schemas/
│   ├── websocket/
│   ├── middleware/
│   ├── dependencies/
│   ├── utils/
│   ├── uploads/
│   ├── tasks/
│   └── main.py
│
├── alembic/
├── tests/
├── docker/
├── nginx/
├── scripts/
├── docs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── alembic.ini
└── README.md
```

---

# Architecture

```text
                Client (Flutter/Web)
                        │
                REST API + WebSocket
                        │
                  FastAPI Application
                        │
        ┌───────────────┼───────────────┐
        │               │               │
 Authentication     Chat Service    User Service
        │               │               │
        └───────────────┼───────────────┘
                        │
                Repository Layer
                        │
        ┌───────────────┼───────────────┐
        │                               │
 PostgreSQL                       Redis Pub/Sub
        │                               │
   Persistent Data             Real-Time Events
```

---

#  Installation

## Clone Repository

```bash
git clone https://github.com/your-username/real-time-chat-app.git

cd real-time-chat-app
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```env
APP_NAME=Realtime Chat

DEBUG=True

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

DATABASE_URL=postgresql+asyncpg://postgres:password@localhost/chat_db

REDIS_URL=redis://localhost:6379

AWS_ACCESS_KEY=

AWS_SECRET_KEY=

AWS_BUCKET=

AWS_REGION=
```

---

# Database Migration

```bash
alembic upgrade head
```

---

# Run Development Server

```bash
uvicorn app.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

Redoc:

```
http://127.0.0.1:8000/redoc
```

---

# Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

Detached Mode

```bash
docker compose up -d
```

Stop

```bash
docker compose down
```

---

# API Modules

* Authentication
* Users
* Chat
* Groups
* Messages
* File Upload
* Notifications
* Health Check

---

# Authentication Flow

```text
Signup

↓

Hash Password

↓

Store User

↓

Login

↓

Generate Access Token

↓

Generate Refresh Token

↓

Protected APIs

↓

Refresh Token

↓

New Access Token
```

---

# WebSocket Flow

```text
User Connects

↓

JWT Verification

↓

Connection Manager

↓

Store Active Connection

↓

Receive Message

↓

Redis Pub/Sub

↓

Broadcast

↓

Store in PostgreSQL

↓

Read Receipt

↓

Typing Status

↓

Disconnect
```

---

# Security

* JWT Authentication
* Password Hashing
* Environment Variables
* Input Validation
* File Validation
* SQL Injection Protection
* CORS Protection
* Secure Dependency Injection
* Repository Pattern
* Centralized Exception Handling

---

# Testing

Run all tests

```bash
pytest
```

Run with coverage

```bash
pytest --cov=app
```

---

# Deployment

Deployment-ready configuration includes:

* Docker
* Docker Compose
* AWS EC2
* Nginx
* HTTPS
* Gunicorn/Uvicorn
* CI/CD Ready Structure

---

# Future Improvements

* Voice Calling
* Video Calling
* Message Reactions
* Emoji Support
* Message Search
* Pinned Messages
* Message Forwarding
* Offline Synchronization
* End-to-End Encryption
* Multi-Device Login

---

# Learning Outcomes

This project demonstrates practical experience with:

* FastAPI
* Async Programming
* SQLAlchemy 2.0
* Repository Pattern
* Service Layer
* Dependency Injection
* JWT Authentication
* PostgreSQL
* Redis
* WebSockets
* Docker
* AWS Deployment
* Production-Level Backend Development

---

 

**Production-Ready Real-Time Chat & Collaboration Backend**

Developed a scalable real-time messaging platform using FastAPI, PostgreSQL, Redis, SQLAlchemy 2.0, WebSockets, Docker, and JWT authentication. Implemented Clean Architecture, Repository Pattern, Service Layer, asynchronous APIs, Redis Pub/Sub, background tasks, image uploads, and production-ready deployment on AWS with Docker and Nginx.

---

# License

This project is intended for educational and portfolio purposes.

---

# Author

**MAYANK AHUJA**

Backend Developer | Python | FastAPI | PostgreSQL | Redis | Docker | AWS

Feel free to fork, star, and contribute to the project.
