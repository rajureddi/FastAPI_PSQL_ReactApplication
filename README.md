

---

# 📦 Product Trac – Full Stack CRUD Application

Product Trac is a full-stack web application built using **React**, **FastAPI**, and **PostgreSQL**.
It demonstrates clean backend API design, database integration, frontend error handling, and real-world full-stack workflows.

---

## 🚀 Features

* Add, update, delete, and view products
* Search products by **ID** or **Name**
* Primary key protection (ID cannot be edited)
* Backend validation with proper HTTP status codes
* Frontend error handling (no console noise)
* PostgreSQL database persistence
* CORS-enabled API for frontend integration

---

## 🛠️ Tech Stack

### Frontend

* React (Hooks)
* HTML5, CSS3
* Fetch API

### Backend

* FastAPI
* SQLAlchemy ORM
* Pydantic
* Uvicorn

### Database

* PostgreSQL

---

## 🧱 Project Architecture

```
React (Frontend)
   ↓ HTTP
FastAPI (Backend)
   ↓ ORM
PostgreSQL (Database)
```

---

## 📂 Folder Structure

```
product-trac/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── database_model.py
│   └── model.py
│
└── frontend/
    ├── src/
    │   ├── App.js
    │   └── App.css
    └── package.json
```

---

## ⚙️ Backend Setup (FastAPI)

### 1️⃣ Create Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 2️⃣ Install Dependencies

```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary
```

### 3️⃣ Configure Database

Edit `database.py`:

```python
db_url = "postgresql://postgres:12345678@localhost:5432/Learning"
```

Make sure PostgreSQL is running and database exists.

---

### 4️⃣ Run Backend

```bash
uvicorn main:app --reload --port 5000
```

Swagger UI:

```
http://127.0.0.1:5000/docs
```

---

## 🌐 API Endpoints

| Method | Endpoint            | Description       |
| ------ | ------------------- | ----------------- |
| GET    | `/all products`     | Get all products  |
| GET    | `/products/{id}`    | Get product by ID |
| POST   | `/products`         | Add new product   |
| PUT    | `/products?id={id}` | Update product    |
| DELETE | `/products?id={id}` | Delete product    |

---

## 💻 Frontend Setup (React)

### 1️⃣ Install Dependencies

```bash
npm install
```

### 2️⃣ Start Frontend

```bash
npm start
```

Frontend runs at:

```
http://localhost:3000
```

---

## 🔐 Validation & Error Handling

### Backend

* Duplicate ID → **409 Conflict**
* Product not found → **404 Not Found**
* Invalid data → **422 Unprocessable Entity**

### Frontend

* Shows user-friendly error messages
* No backend errors exposed in console
* Prevents invalid numeric input

---


## 🧠 Key Learning Outcomes

* Full-stack communication using REST APIs
* Proper database integrity enforcement
* Frontend-backend error contract handling
* Real-world CRUD architecture
* Clean separation of concerns

---

## 📦 Future Enhancements

* Auto-generated product IDs
* Pagination & sorting
* Authentication (JWT)
* Dockerized deployment
* AI-powered product search (RAG)

---

## 👤 Author

**Raju Bandam**
B.Tech – Computer Science Engineering
Full-Stack & AI Enthusiast

---

## 🔥 Final Note

This project is **part of LEARNING FastAPI,PostgreSQL

---
