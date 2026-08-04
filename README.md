# 🎧 Spotify Clone — Backend

A RESTful backend API for a Spotify-style music streaming app, built with **FastAPI** and **PostgreSQL**. It handles user authentication, song uploads (via Cloudinary), and a favourites system — everything a music-streaming client needs on the server side.

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)

---

## 📖 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Server](#running-the-server)
- [API Reference](#-api-reference)
- [Data Models](#-data-models)
- [Screenshots](#-screenshots)
- [Security Notes](#-security-notes)
- [Roadmap](#-roadmap)

---

## ✨ Features

- 🔐 **User authentication** — sign up / log in with hashed passwords (`bcrypt`) and JWT-based sessions
- 🎵 **Song upload** — songs and thumbnails are uploaded directly to **Cloudinary**
- ❤️ **Favourites system** — toggle songs in/out of a user's favourites list
- 📄 **Auto-generated API docs** — interactive Swagger UI out of the box (thanks to FastAPI)
- 🗄️ **PostgreSQL + SQLAlchemy ORM** — clean, relational data modeling with `User`, `Song`, and `Favourite`

---

## 🛠 Tech Stack

| Layer            | Technology                          |
|-------------------|--------------------------------------|
| Framework         | [FastAPI](https://fastapi.tiangolo.com/) |
| Language          | Python 3.14                          |
| Database          | PostgreSQL                           |
| ORM               | SQLAlchemy                           |
| Auth              | JWT (`PyJWT`) + `bcrypt` password hashing |
| Media Storage     | Cloudinary                           |
| Server            | Uvicorn (ASGI)                       |
| Validation        | Pydantic                             |

---

## 📁 Project Structure

```
spotify_clone_backend/
│
├── main.py                        # FastAPI app entry point & router registration
├── database.py                    # SQLAlchemy engine, session, and DB dependency
├── .env                           # Environment variables (not committed)
├── .gitignore
│
├── middleware/
│   └── auth_middleware.py         # JWT verification dependency (x-auth-token header)
│
├── models/                        # SQLAlchemy ORM models
│   ├── base.py                    # Declarative Base
│   ├── user.py                    # User table
│   ├── song.py                    # Song table
│   └── favourite.py                # Favourite (join table: user ↔ song)
│
├── pydantic_schemas/               # Request/response validation schemas
│   ├── user_create.py             # Sign-up payload
│   ├── user_login.py              # Login payload
│   └── favourite_song.py          # Favourite toggle payload
│
├── routes/                        # API route handlers
│   ├── auth.py                    # /auth  → signUp, login, current user
│   └── song.py                    # /song  → upload, list, favourite, favourites
│
└── screenshots/                   # API testing & docs screenshots (see below)
```

> **Note:** the repo also contains a `venv/` folder with the local virtual environment. This should normally be excluded via `.gitignore` and is not part of the application logic.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+ (project was built/tested on 3.14)
- PostgreSQL server running locally or remotely
- A free [Cloudinary](https://cloudinary.com/) account (for media uploads)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mohamadnafe14-arch/spotify-clone-backend-.git
cd spotify_clone_backend

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic \
            python-dotenv pyjwt bcrypt cloudinary python-multipart
```

> 💡 Tip: once your environment is finalized, generate a proper `requirements.txt` with `pip freeze > requirements.txt` so others can install everything with one command.

### Environment Variables

Create a `.env` file in the project root with your Cloudinary credentials:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

You'll also need a PostgreSQL database named `spotify` (or update the connection string — see [Security Notes](#-security-notes)).

### Running the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, and the interactive Swagger docs at:

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Reference

### Auth — `/auth`

| Method | Endpoint       | Auth Required | Description                          |
|--------|----------------|:--------------:|---------------------------------------|
| POST   | `/auth/signUp` | ❌              | Create a new user account             |
| POST   | `/auth/login`  | ❌              | Log in and receive a JWT token        |
| GET    | `/auth/`       | ✅              | Get the currently authenticated user  |

### Songs — `/song`

| Method | Endpoint          | Auth Required | Description                                  |
|--------|-------------------|:--------------:|------------------------------------------------|
| POST   | `/song/upload`    | ✅              | Upload a song + thumbnail (multipart/form-data) |
| GET    | `/song/`          | ✅              | Get all songs                                  |
| POST   | `/song/favourite` | ✅              | Toggle a song in the user's favourites         |
| GET    | `/song/favourites`| ✅              | Get the current user's favourite songs         |

> All protected routes expect an **`x-auth-token`** header containing the JWT returned from sign-up/login.

---

## 🗃 Data Models

**User**
| Field | Type |
|---|---|
| id | TEXT (UUID, PK) |
| name | VARCHAR(100) |
| email | VARCHAR(100) |
| password | BYTEA (bcrypt hash) |

**Song**
| Field | Type |
|---|---|
| id | TEXT (UUID, PK) |
| song_name | VARCHAR(100) |
| artist | VARCHAR(100) |
| color_hex | VARCHAR(6) |
| thumbnail_url | TEXT |
| song_url | TEXT |

**Favourite** (join table)
| Field | Type |
|---|---|
| id | TEXT (UUID, PK) |
| user_id | TEXT (FK → users.id) |
| song_id | TEXT (FK → songs.id) |

---

## 🖼 Screenshots

The `screenshots/` folder documents the API being tested end-to-end via the auto-generated Swagger UI (`/docs`) — covering sign-up, login, song upload, listing songs, and the favourites flow, along with the resulting media assets stored on Cloudinary.

### Authentication Endpoints

**Sign Up — POST `/auth/signUp`**
![Sign Up endpoint](./screenshots/Screenshot%202026-08-04%20134954.png)
Sign up creates a new user and returns a JWT token + user details. Password is hashed with bcrypt before storage.

**Sign Up Response**
![Sign Up response with JWT token](./screenshots/Screenshot%202026-08-04%20135216.png)
The response includes the generated JWT token and all user information.

**Login — POST `/auth/login`**
![Login endpoint](./screenshots/Screenshot%202026-08-04%20135646.png)
Login with email and password, receive a JWT token to use in subsequent requests.

**Get Current User — GET `/auth/`**
![Get current user endpoint](./screenshots/Screenshot%202026-08-04%20141637.png)
Fetch the currently authenticated user's profile by passing the JWT in the `x-auth-token` header.

### Song Management Endpoints

**Upload Song — POST `/song/upload`**
![Upload song endpoint](./screenshots/Screenshot%202026-08-04%20141735.png)
Upload a song file and thumbnail image. Both are stored on Cloudinary, URLs saved in the database.

**Get All Songs — GET `/song/`**
![Get songs endpoint](./screenshots/Screenshot%202026-08-04%20142013.png)
Retrieve all songs in the system with pagination support. Authentication required.

**Songs Response (JSON Example)**
![Songs response data](./screenshots/Screenshot%202026-08-04%20142419.png)
Returns a list of songs with metadata: song name, artist, color hex, thumbnail URL, and song URL.

**Toggle Favourite — POST `/song/favourite`**
![Favourite endpoint](./screenshots/Screenshot%202026-08-04%20142707.png)
Add or remove a song from the user's favourites by passing the song ID.

**Get User Favourites — GET `/song/favourites`**
![Get favourites endpoint](./screenshots/Screenshot%202026-08-04%20142819.png)
Fetch all songs marked as favourites by the current user.

### Pydantic Schemas

**API Request/Response Schemas**
![Schemas documentation](./screenshots/Screenshot%202026-08-04%20143143.png)
Pydantic automatically validates and documents all request/response structures (UserCreate, UserLogin, FavouriteSong, etc.).

### Cloudinary Media Assets

**Media Library — 80+ Assets**
![Cloudinary media library](./screenshots/Screenshot%202026-08-04%20143455.png)
Songs and thumbnails uploaded via the `/song/upload` endpoint are stored in Cloudinary's media library for fast CDN delivery.

---

## 🔒 Security Notes

A few things worth fixing before deploying this to production:

- **Hardcoded DB credentials**: `database.py` currently has the PostgreSQL connection string (including the password) hardcoded. Move this into `.env` and load it via `os.getenv("DATABASE_URL")`, just like the Cloudinary config already does.
- **Hardcoded JWT secret**: the string `"secret"` is used to sign/verify JWTs in `auth.py` and `auth_middleware.py`. Move this to an environment variable (e.g. `JWT_SECRET`) and use a long, random value.
- **`.env` is already git-ignored** ✅ — keep it that way, and never commit real credentials.

---

## 🗺 Roadmap

- [ ] Add a `requirements.txt` / `pyproject.toml`
- [ ] Move all secrets (DB URL, JWT secret) into environment variables
- [ ] Add playlist support
- [ ] Add pagination to `/song/`
- [ ] Add automated tests (pytest + FastAPI `TestClient`)
- [ ] Dockerize the app

---

## 👤 Author

**Mohamed Nafeh**
GitHub: [@mohamadnafe14-arch](https://github.com/mohamadnafe14-arch)
