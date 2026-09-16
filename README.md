# Task Management System

A Django-based Task Management System that provides secure RESTful APIs and a Django template-based web interface for managing personal tasks.

The application supports user registration, JWT authentication, task creation, task updates, task deletion, task status and priority management, due dates, and owner-based access control.

## 🚀 Live Demo

**Live Application:**
https://task-management-system-vt8b.onrender.com/

> The application is deployed on Render.

## 📌 Project Overview

The Task Management System is a backend-focused web application built with **Python, Django, and Django REST Framework**.

It provides two ways to interact with the system:

1. **RESTful API** — for creating and managing tasks using API clients such as Postman.
2. **Django Web Interface** — for user registration, login, dashboard access, and task management through Django templates.

Each authenticated user can access and manage their own tasks. The API uses **JWT authentication**, while task-level access is protected using a custom owner permission.

## ✨ Features

### Authentication

* User registration
* JWT-based authentication
* Access token and refresh token
* Token refresh endpoint
* Protected API endpoints
* Django session-based web login

### Task Management

* Create tasks
* View all tasks belonging to the authenticated user
* View an individual task
* Update tasks using PUT
* Partially update tasks using PATCH
* Delete tasks
* Task ownership protection

### Task Information

Each task can contain:

* Title
* Description
* Status
* Priority
* Due date
* Created by
* Created timestamp

### Task Status

Tasks support three statuses:

* `pending`
* `in_progress`
* `completed`

### Task Priority

Tasks support three priority levels:

* `low`
* `medium`
* `high`

### Web Interface

The project also includes Django template-based pages for:

* User registration
* Login
* Dashboard
* Add task
* Edit task
* Delete task
* Logout

## 🛠️ Tech Stack

| Technology            | Purpose                                      |
| --------------------- | -------------------------------------------- |
| Python                | Programming language                         |
| Django                | Web framework                                |
| Django REST Framework | REST API development                         |
| Simple JWT            | JWT authentication                           |
| SQLite                | Default database                             |
| PostgreSQL            | Supported through database URL configuration |
| HTML                  | Web interface                                |
| CSS                   | Web interface styling                        |
| Django Templates      | Server-side frontend                         |
| WhiteNoise            | Static file serving                          |
| Gunicorn              | Production WSGI server                       |
| Render                | Deployment                                   |
| Postman               | API testing                                  |

## 📂 Project Structure

```text
Task-management-System/
│
├── student/
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── serializers.py
│   ├── permissions.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── students/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── staticfiles/
├── build.sh
├── manage.py
├── requirements.txt
├── db.sqlite3
└── README.md
```

## 🔐 Authentication Flow

The API uses JWT authentication through Django REST Framework Simple JWT.

### 1. Register

**POST**

```text
/student/register/
```

Request body:

```json
{
    "username": "abhishek",
    "email": "abhishek@example.com",
    "password": "YourStrongPassword123"
}
```

Successful response:

```json
{
    "message": "User registered successfully"
}
```

### 2. Login

**POST**

```text
/student/login/
```

Request body:

```json
{
    "username": "abhishek",
    "password": "YourStrongPassword123"
}
```

The login endpoint returns an access token and refresh token.

Example:

```json
{
    "refresh": "your-refresh-token",
    "access": "your-access-token"
}
```

### 3. Send Access Token

For protected endpoints, add the access token to the request header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 🔗 API Endpoints

### Authentication

| Method | Endpoint                  | Authentication | Description          |
| ------ | ------------------------- | -------------- | -------------------- |
| POST   | `/student/register/`      | No             | Register a new user  |
| POST   | `/student/login/`         | No             | Obtain JWT tokens    |
| POST   | `/student/token/refresh/` | No             | Refresh access token |

### Tasks

| Method | Endpoint               | Authentication | Description             |
| ------ | ---------------------- | -------------- | ----------------------- |
| GET    | `/student/tasks/`      | JWT            | Get user's tasks        |
| POST   | `/student/tasks/`      | JWT            | Create a task           |
| GET    | `/student/tasks/<id>/` | JWT            | Get a specific task     |
| PUT    | `/student/tasks/<id>/` | JWT            | Replace a task          |
| PATCH  | `/student/tasks/<id>/` | JWT            | Partially update a task |
| DELETE | `/student/tasks/<id>/` | JWT            | Delete a task           |

These routes are defined in the project's URL configuration.

## 📝 Create Task

**POST**

```text
/student/tasks/
```

Headers:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json
```

Request body:

```json
{
    "title": "Complete Django API",
    "description": "Build and test the task management API",
    "status": "pending",
    "priority": "high",
    "due_date": "2026-09-30"
}
```

The authenticated user is automatically stored as the task owner.

## 📋 Get Tasks

**GET**

```text
/student/tasks/
```

Header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

The API returns only tasks created by the authenticated user.

## 🔎 Get Task by ID

**GET**

```text
/student/tasks/1/
```

Header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Replace `1` with the required task ID.

## ✏️ Update Task

### PUT

```text
/student/tasks/1/
```

Example body:

```json
{
    "title": "Complete Django REST API",
    "description": "Complete API development and testing",
    "status": "in_progress",
    "priority": "high",
    "due_date": "2026-10-01"
}
```

### PATCH

PATCH can be used when only selected fields need to be changed.

Example:

```json
{
    "status": "completed"
}
```

## 🗑️ Delete Task

**DELETE**

```text
/student/tasks/1/
```

Header:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

A successful deletion returns a `204 No Content` response.

## 🔒 Authorization & Ownership

Task APIs require authentication.

The application uses:

```text
JWTAuthentication
```

for API authentication.

Task detail operations also use a custom `IsOwner` permission. A user can only access their own task records.

The API filters task lists using the authenticated user and checks task ownership for individual operations.

## 🗃️ Task Model

The Task model contains the following fields:

| Field         | Type          | Description               |
| ------------- | ------------- | ------------------------- |
| `title`       | CharField     | Task title                |
| `description` | TextField     | Task description          |
| `status`      | CharField     | Current task status       |
| `priority`    | CharField     | Task priority             |
| `due_date`    | DateField     | Optional deadline         |
| `created_by`  | ForeignKey    | User who created the task |
| `created_at`  | DateTimeField | Task creation timestamp   |

The available status and priority choices are defined in the Django model.

## 🌐 Web Interface

The project includes a Django template-based interface.

Available pages include:

```text
/student/web/register/
/student/web/login/
/student/web/dashboard/
/student/web/task/add/
/student/web/task/edit/<id>/
/student/web/task/delete/<id>/
/student/web/logout/
```

The dashboard displays the authenticated user's tasks and task statistics.

## 💻 Local Installation

### Prerequisites

Make sure you have:

* Python 3.10+
* Git
* pip
* Virtual environment

### 1. Clone the Repository

```bash
git clone https://github.com/Abhishek-Chauhan5/Task-management-System.git
```

### 2. Enter the Project

```bash
cd Task-management-System
```

### 3. Create Virtual Environment

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## 🧪 Testing with Postman

You can test the REST APIs using Postman.

### Recommended testing sequence

```text
1. Register user
        ↓
2. Login
        ↓
3. Copy access token
        ↓
4. Add Bearer Token
        ↓
5. Create task
        ↓
6. Get tasks
        ↓
7. Update task
        ↓
8. Partially update task
        ↓
9. Delete task
```

For protected requests, use:

```text
Authorization
Type: Bearer Token
Token: YOUR_ACCESS_TOKEN
```

## ☁️ Deployment

The application is configured for deployment on Render.

The repository contains a `build.sh` script that installs Python dependencies, collects static files, and runs database migrations.

### Render Build Command

```bash
./build.sh
```

### Render Start Command

```bash
gunicorn students.wsgi:application
```

### Production Environment Variables

Recommended environment variables:

```text
DEBUG=False
SECRET_KEY=your-production-secret-key
```

If using an external PostgreSQL database:

```text
DATABASE_URL=your-database-url
```

### Production DEBUG Setting

For production, use:

```python
DEBUG = os.environ.get("DEBUG", "False") == "True"
```

Do not use a default of `True` in production.

## ⚙️ Production Configuration

The project already uses:

* `dj-database-url` for database URL configuration
* WhiteNoise for static files
* Gunicorn for production serving
* `ALLOWED_HOSTS` configured for Render
* `collectstatic` during deployment

The current repository uses SQLite as the fallback database when `DATABASE_URL` is not provided.

## 📁 Static Files

Static files are configured using WhiteNoise.

The production static root is:

```text
staticfiles/
```

The deployment script runs:

```bash
python manage.py collectstatic --no-input
```

## 🔑 Environment Variables

Create a `.env` file for local development if desired:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=
```

Do not commit real secrets, passwords, API keys, or production credentials to GitHub.

## 🔧 Future Improvements

Possible improvements for future versions:

* PostgreSQL as the primary production database
* API documentation with Swagger/OpenAPI
* Pagination
* Task filtering and search
* Task sorting
* Email notifications
* Password reset
* User profile management
* Docker support
* Automated tests
* CI/CD with GitHub Actions
* API rate limiting

## 📚 Learning Outcomes

This project demonstrates practical experience with:

* Django project structure
* Django ORM
* Django models
* REST API development
* APIView
* Serializers
* JWT authentication
* Custom permissions
* CRUD operations
* HTTP status codes
* Django templates
* Authentication and authorization
* Database configuration
* Static file handling
* Production deployment
* Render deployment
* API testing with Postman

## 👨‍💻 Author

**Abhishek Singh Chauhan**

* GitHub: https://github.com/Abhishek-Chauhan5
* LinkedIn: https://www.linkedin.com/in/abhishekchauhan0514/

## 📄 License

This project is available for educational and portfolio purposes.
