# 📘 Mini RAG - Question Answering System

A minimal implementation of a **Retrieval-Augmented Generation (RAG)** model for question answering built with **FastAPI**.

---

## 🚀 Requirements

- Python 3.11
- Docker & Docker Compose
- PostgreSQL (if running locally)
- Linux / macOS (Windows via WSL recommended)

---

## 🧰 System Dependencies (Required for psycopg2)

If you face issues installing `psycopg2`, run:

```bash
sudo apt update
sudo apt install libpq-dev gcc python3-dev
```

---

## 🐍 Setup Python Environment (Using Miniconda)

### 1️⃣ Install Miniconda

Download and install Miniconda from:  
https://docs.conda.io/en/latest/miniconda.html

---

### 2️⃣ Create a New Environment

```bash
conda create -n mini-rag python=3.11
```

### 3️⃣ Activate the Environment

```bash
conda activate mini-rag
```

---

## 📦 Installation

Install required packages:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables Setup

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```
OPENAI_API_KEY=your_openai_key
DATABASE_URL=your_database_url
APP_NAME=Mini RAG
APP_VERSION=0.1
```

---

## 🐳 Run Docker Services

```bash
cd docker
cp .env.example .env
```

Update `docker/.env` with your credentials.

Start services:

```bash
sudo docker compose up -d
```

---

## 🗄️ Run Alembic Migrations

### Configure Alembic

```bash
cp alembic.ini.example alembic.ini
```

Update:

```
sqlalchemy.url = your_database_url
```

### (Optional) Create New Migration

```bash
alembic revision --autogenerate -m "Add new feature"
```

### Apply Migrations

```bash
alembic upgrade head
```

---

## ▶️ Run the FastAPI Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 5050
```

Server will be available at:

```
http://localhost:5050
```

Swagger documentation:

```
http://localhost:5050/docs
```

---

## 🏗️ Project Structure

```
mini-rag/
│
├── main.py
├── routes/
├── models/
├── docker/
├── alembic/
├── requirements.txt
└── .env.example
```

---

## ✅ Notes

- Make sure Docker is running before starting services.
- Ensure `.env` variables are properly configured.
- If port 5050 is already in use, change the port (e.g., 5080).

---

## 📄 License

This project is for educational purposes.
