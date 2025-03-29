# Household Services App

## Description

Household Services App is a multi-user platform for booking and managing home services. It provides features for customers to request services, professionals to accept/reject requests, and admins to oversee operations. The project includes user authentication, service management, and asynchronous task handling.

## Technologies Used

- **Backend**: Python, Flask, Celery, SQLite
- **Frontend**: Visual Basic, React (requires npm)
- **Environment**: Ubuntu (WSL recommended)
- **Asynchronous Tasks**: Celery, Redis, Mailhog

## Installation & Setup

### Prerequisites

Ensure you have the following installed:

- **Python** (>=3.8)
- **Flask**
- **Visual Basic**
- **SQLite**
- **Node.js & npm** (for frontend)
- **Redis** (for Celery tasks)
- **Mailhog** (for email testing)
- **Ubuntu/WSL** (for running the app)

### Installation Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/household-services-app.git
   cd household-services-app
   ```
2. Install backend dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```sh
   cd frontend
   npm install
   ```
4. Set up SQLite database:
   ```sh
   python3 setup_db.py
   ```
5. Configure environment variables (create a `.env` file and add necessary keys like database URLs, API keys, etc.).

## Running the Project

### Running the Frontend

1. Open a **WSL terminal** and navigate to the frontend folder:
   ```sh
   cd frontend
   npm run dev
   ```

### Running Celery for Synchronous Tasks

In a **WSL terminal**, run the following in the backend folder:

```sh
celery -A main.celery worker --loglevel=info
```

In another **WSL terminal**, run:

```sh
celery -A main.celery beat --loglevel=info
```

### Running Asynchronous Export Function

Open **4 WSL terminals** and run the following:

1. **Start Mailhog** (Terminal 1):
   ```sh
   mailhog
   ```
2. **Start Redis Server** (Terminal 2):
   ```sh
   redis-server
   ```
3. **Run Flask Backend** (Terminal 3):
   ```sh
   python3 main.py
   ```
4. **Run Celery Worker** (Terminal 4):
   ```sh
   celery -A main.celery worker --loglevel=info
   ```

Access Celery functions at:
[http://localhost:8025/](http://localhost:8025/)

## Project Structure

```
/household-services-app
│-- backend/
│   │--main.py (Flask app)
│   │-- models.py (Database models)
│   │-- tasks.py (Celery tasks)
│   │-- applications/
│   └── .env
│-- frontend/
│   │-- src/
│   │-- public/
│   │-- package.json
│   └── index.html
│-- README.md
```

## Troubleshooting

- If Celery is not working, ensure **Redis** is running (`redis-server`).
- If frontend doesn't start, check `npm install` is completed.
- If Mailhog UI doesn't load, verify `mailhog` is running.
- Check logs for errors in each terminal.





