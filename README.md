# Task Manager - Login Authentication + Todo List

A full-stack web application built with Flask and MySQL that implements user authentication with registration, login, profile management, and a personal todo list.

## 🌟 Features

### Authentication
- **User Registration** - Secure account creation with email validation and password confirmation
- **User Login** - Session-based authentication with bcrypt password hashing
- **Profile Management** - Update name, email, and password with validation
- **Session Management** - Automatic logout and login state tracking

### Todo List Management
- **Create Tasks** - Add new tasks with title and description
- **View Tasks** - See all your tasks with creation dates and current status
- **Update Status** - Cycle task status: Pending → Working → Completed → Pending
- **Delete Tasks** - Remove individual tasks or clear all tasks at once
- **Status Tracking** - Three task statuses: Pending, Working, Completed
- **User-Specific** - Each user only sees their own tasks (secure)

### Security Features
- **Password Hashing** - Passwords hashed with bcrypt before storage
- **CSRF Protection** - All forms include CSRF tokens via Flask-WTF
- **Session Management** - Flask-Login manages secure sessions
- **SQL Injection Prevention** - SQLAlchemy ORM prevents SQL injection
- **Email Validation** - Email format and uniqueness validated
- **Protected Routes** - Dashboard and profile require authentication
- **User Authorization** - Tasks can only be modified by their creator

## 🛠️ Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login with bcrypt password hashing
- **Forms**: Flask-WTF with WTForms validation
- **Frontend**: Bootstrap 4, Jinja2 templating
- **Security**: CSRF tokens, password hashing

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- pip (Python package manager)

## 🚀 Installation

### 1. Clone/Download the Project
```bash
cd "Login Auth Project"
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Database

Create a MySQL database:
```sql
CREATE DATABASE vanshdb;
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here-change-this
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=vanshdb
FLASK_ENV=development
```

**Important**: Replace the values with your actual MySQL credentials and generate a strong secret key. The app will use `DB_NAME` to connect to the correct database. If `DB_NAME` is omitted, it defaults to `vanshdb`.

### 6. Initialize Database Tables

In Python shell:
```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.create_all()
```

## 📁 Project Structure

```
Login Auth Project/
├── run.py                 # Application entry point
├── .env                   # Environment variables (not in git)
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── app/
    ├── __init__.py       # Flask app factory
    ├── forms.py          # WTForms validation forms
    ├── models/           # Database models (organized)
    │   ├── __init__.py   # Exports User and Task models
    │   ├── user.py       # User model for authentication
    │   └── task.py       # Task model for todos
    ├── routes/           # Route handlers (organized)
    │   ├── __init__.py   # Registers blueprints
    │   ├── auth.py       # Authentication routes (register, login, logout, profile)
    │   └── tasks.py      # Task routes (create, read, update, delete)
    └── templates/
        ├── base.html     # Base template with navigation
        ├── index.html    # Home page
        ├── login.html    # Login form
        ├── register.html # Registration form
        ├── dashboard.html# User dashboard with tasks
        └── profile.html  # Profile edit form
```

**Architecture Benefits:**
- ✅ **Scalable** - Easy to add new routes or models
- ✅ **Organized** - Clear separation of concerns
- ✅ **Maintainable** - Each file has a single responsibility
- ✅ **Professional** - Industry-standard project structure

## 🎯 Usage

### 1. Run the Application
```bash
python run.py
```

The app will start at `http://localhost:5000`

### 2. Create an Account
- Navigate to the Register page
- Fill in name, email, and password
- Passwords must match for confirmation
- Account created message will appear

### 3. Login
- Use your registered email and password
- Upon success, you'll be redirected to the dashboard

### 4. Manage Your Tasks
- **View Tasks**: All your tasks appear on the dashboard
- **Add Task**: Type task title and click "Add Task"
- **Update Status**: Click "📌 Update" button to cycle status
  - Pending (⏳) → Working (⚡) → Completed (✓) → Pending
- **Delete Task**: Click "🗑️ Delete" to remove individual task
- **Clear All**: Click "🧹 Clear All Tasks" to delete everything

### 5. Update Profile
- Click the "Profile" button in the navigation
- Update name, email, or password
- Changes are saved immediately

### 6. Logout
- Click the "Logout" button in the navigation
- Session will be cleared

## 🔐 Security Features

- **Password Hashing**: Passwords are hashed with bcrypt before storage
- **CSRF Protection**: All forms include CSRF tokens via Flask-WTF
- **Session Management**: Flask-Login manages secure sessions
- **SQL Injection Prevention**: SQLAlchemy ORM prevents SQL injection
- **Email Validation**: Email format and uniqueness validated
- **Protected Routes**: Dashboard and profile require authentication

## 📚 API Routes

### Authentication Routes
| Route | Method | Description | Auth Required |
|-------|--------|-------------|---|
| `/` | GET | Home page | No |
| `/register` | GET, POST | User registration | No |
| `/login` | GET, POST | User login | No |
| `/dashboard` | GET | User dashboard with tasks | Yes |
| `/profile` | GET, POST | Edit user profile | Yes |
| `/logout` | GET | Logout user | Yes |

### Task Routes (NEW!)
| Route | Method | Description | Auth Required |
|-------|--------|-------------|---|
| `/tasks/add` | POST | Create a new task | Yes |
| `/tasks/update/<id>` | POST | Change task status | Yes |
| `/tasks/delete/<id>` | POST | Delete a specific task | Yes |
| `/tasks/clear` | POST | Delete all tasks | Yes |

## 🔄 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

### Tasks Table (NEW!)
```sql
CREATE TABLE tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**Key Relationship:**
- One User can have Many Tasks (1:N relationship)
- Tasks are linked to users via `user_id` foreign key
- When a user is deleted, all their tasks are automatically deleted (CASCADE)

## 🚨 Common Issues

### Issue: "No module named 'mysqlclient'"
**Solution**: Install MySQL dev libraries and reinstall:
```bash
pip install --upgrade mysqlclient
```

### Issue: Database connection refused
**Solution**: Ensure MySQL is running and credentials in `.env` are correct:
```bash
# Check MySQL service is running (Windows)
net start MySQL80

# Or start MySQL (macOS with Homebrew)
brew services start mysql
```

### Issue: "SECRET_KEY not found"
**Solution**: Make sure `.env` file exists and contains `SECRET_KEY=your-key`

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [OWASP Security Guidelines](https://owasp.org/www-project-web-security-testing-guide/)

## 🚀 Deployment

To deploy this application:

1. **Set `debug=False` in run.py** for production
2. **Use a production WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 run:app
   ```
3. **Use a reverse proxy** like Nginx
4. **Enable HTTPS** with SSL certificates
5. **Deploy to platforms** like:
   - Heroku
   - AWS (EC2, RDS)
   - DigitalOcean
   - PythonAnywhere
   - Railway
   - Render

## 📈 Future Improvements

- [ ] Email verification on registration
- [ ] Password reset functionality via email
- [ ] Two-factor authentication (2FA)
- [ ] Social login (Google, GitHub OAuth)
- [ ] User avatar/profile picture upload
- [ ] Account deletion functionality
- [ ] Admin dashboard for user management
- [ ] Unit tests and integration tests
- [ ] API endpoints (REST API)
- [ ] Rate limiting on login attempts
- [ ] Activity logging
- [ ] Remember me functionality

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created as a learning project demonstrating Flask authentication best practices.

---

**Note**: This is a learning project. For production use, review security best practices and implement additional safeguards as needed.
