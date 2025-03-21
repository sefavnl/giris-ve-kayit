# User Authentication System

A complete user authentication system with React.js frontend, FastAPI backend, and MongoDB database.

## Project Structure

```
project/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── routes.py
│   ├── __init__.py
│   └── requirements.txt
│
└── frontend/
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── components/
    │   │   ├── Dashboard.js
    │   │   ├── Login.js
    │   │   ├── PrivateRoute.js
    │   │   └── Register.js
    │   ├── context/
    │   │   └── AuthContext.js
    │   ├── services/
    │   │   └── api.js
    │   ├── App.css
    │   ├── App.js
    │   └── index.js
    └── package.json
```

## Features

- User registration with email validation
- User login with JWT authentication
- Protected routes for authenticated users
- Form validation and error handling
- Modern UI with responsive design

## Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Run the server:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at: http://localhost:8000

API Documentation at: http://localhost:8000/docs

## Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Run the development server:
   ```
   npm start
   ```

The frontend will be available at: http://localhost:3000

## API Endpoints

- `POST /api/register`: Register a new user
- `POST /api/login`: Login a user
- `GET /api/users/me`: Get the current user's information (requires authentication)

## Technologies Used

- **Frontend**: React.js, React Router, Axios
- **Backend**: FastAPI, PyMongo
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: MongoDB
- **Styling**: CSS 