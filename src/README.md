# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- Teacher-only student registration and removal
- Teacher login backed by hashed credentials and signed sessions

## Getting Started

1. Install the dependencies from the repository root:

   ```
   pip install -r requirements.txt
   ```

2. Create a teacher account (repeat for each teacher):

   ```
   cd src
   python create_teacher.py staff
   cd ..
   ```

   The password is prompted securely and stored as a salted hash in `src/teachers.json`. This local credentials file is git-ignored. Restart the server after adding an account.

3. Set a persistent session-signing secret and run the application:

   ```
   export SESSION_SECRET="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
   uvicorn app:app --app-dir src --reload
   ```

   Without `SESSION_SECRET`, a random key is generated at startup and teacher sessions end when the server restarts. Set `COOKIE_SECURE=true` when serving over HTTPS.

4. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/auth/status`                                                    | Check whether the current session is a teacher session              |
| POST   | `/auth/login`                                                      | Start a teacher session                                             |
| POST   | `/auth/logout`                                                     | End the current session                                             |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Register a student; teacher login required                         |
| DELETE | `/activities/{activity_name}/unregister?email=student@mergington.edu` | Remove a student; teacher login required                         |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.
