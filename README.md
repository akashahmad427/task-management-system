# Task Management System

A comprehensive Django-based task management system with user authentication, task CRUD operations, and REST API support.

## Features

- **User Management**: User registration, login, and profile management
- **Task Management**: Create, read, update, and delete tasks
- **Category System**: Organize tasks by categories
- **Priority Levels**: Set task priorities (Low, Medium, High)
- **Status Tracking**: Track task completion status
- **REST API**: Full REST API support with Django REST Framework
- **Responsive UI**: Modern, responsive web interface
- **Search & Filter**: Advanced search and filtering capabilities

## Technology Stack

- **Backend**: Django 4.2.11
- **Database**: SQLite (development), PostgreSQL (production ready)
- **API**: Django REST Framework 3.14.0
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication system
- **CORS**: Django CORS Headers for cross-origin requests

## Installation

### Prerequisites

- Python 3.8+
- pip
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <your-github-repo-url>
   cd task-management-system
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
task_management_system/
├── task_management_system/    # Main project settings
├── tasks/                     # Task management app
├── users/                     # User management app
├── templates/                 # HTML templates
├── static/                    # CSS, JS, and images
├── manage.py                  # Django management script
└── requirements.txt           # Python dependencies
```

## API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login
- `GET /api/users/profile/` - User profile

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create new task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **Developer**: Ahmad Akash
- **Email**: ahmadakash427427@gmail.com
- **GitHub**: [@akashahmad427](https://github.com/akashahmad427)

## Acknowledgments

- Django community for the excellent framework
- Django REST Framework team for the powerful API toolkit
- All contributors and supporters of this project 

