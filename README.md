# Notaki

A note-taking REST API built with FastAPI.

## Features

- User registration and login
- JWT authentication
- User authorization
- Create, read, update, delete notes (CRUD Operations)
- PostgreSQL database

## Tech Stack

- FastAPI
- SQLModel
- PostgreSQL (Supabase)
- JWT
- Uvicorn

## Project Structure

```text
Notaki/
│
├── back-end/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── authentication.py
│   ├── crud.py
│   └── routers/
│       ├── auth.py
│       └── notes.py
│
├── front-end/
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── register.js
│       ├── login.js
│       └── dashboard.js
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Security

- **Password Hashing** – User passwords are hashed before storing in the database.
- **JWT Authentication** – Endpoints of Notes needs a valid Web Token to access and modify.
- **Authorization** – Users can only create, read, update, and delete their own notes.


### Authentication Flow

1. User signs up with a username, email, and password.
2. The password is hashed before being stored.
3. The user logs in with valid credentials.
4. The server(back-end) generates a JWT access token.
5. The client(front-end) includes the token in the `Authorization` header for protected requests.
6. The server validates the token and identifies current user.



## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | /signup | Create user account |
| POST | /login | Login and receive JWT |

### Notes

| Method | Endpoint | Description |
|---|---|---|
| GET | /notes | Get user's notes |
| POST | /notes | Create note |
| PUT | /notes/{id} | Update note |
| DELETE | /notes/{id} | Delete note |


## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

Run the server:

```bash
uvicorn main:app --reload
```

## API Documentation

FastAPI has automatic documentation:

```
/docs
```