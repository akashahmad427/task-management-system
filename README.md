# Task Management System

A comprehensive Django-based task management system with role-based permissions, built according to the Django Assignment requirements.

## 🚀 Features

### Core Functionality
- **User Management**: Role-based user system (Admin, Manager, Employee)
- **Task Management**: Full CRUD operations for tasks
- **Role-based Permissions**: Different access levels based on user roles
- **Task Assignment**: Assign tasks to team members
- **Status Tracking**: Track task progress (Pending, In Progress, Review, Completed, Cancelled)
- **Priority Management**: Set task priorities (Low, Medium, High, Urgent)
- **Category System**: Organize tasks by categories
- **Due Date Management**: Set and track task deadlines
- **Time Tracking**: Estimated vs. actual hours
- **Comments System**: Add comments to tasks
- **File Attachments**: Upload files to tasks
- **Search & Filtering**: Advanced task search and filtering
- **Dashboard**: Comprehensive overview with statistics

### User Roles & Permissions

#### Admin
- Full system access
- User management
- Task management
- System settings

#### Manager
- Create and assign tasks
- Manage team tasks
- View all tasks
- Update task status

#### Employee
- View assigned tasks
- Update task status
- Add comments
- Upload attachments

## 🛠️ Technology Stack

- **Backend**: Django 5.2.5
- **Database**: SQLite (can be easily changed to PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Authentication**: Django's built-in authentication system
- **API**: Django REST Framework
- **File Handling**: Django's file storage system
- **Icons**: Font Awesome 6

## 📁 Project Structure

```
Django_Project/
├── task_management_system/     # Main project settings
├── users/                      # User management app
│   ├── models.py              # Custom user model
│   ├── views.py               # User views and API
│   ├── serializers.py         # User serializers
│   ├── forms.py               # User forms
│   ├── admin.py               # Admin configuration
│   └── urls.py                # User URL patterns
├── tasks/                      # Task management app
│   ├── models.py              # Task models
│   ├── views.py               # Task views and API
│   ├── serializers.py         # Task serializers
│   ├── forms.py               # Task forms
│   ├── admin.py               # Admin configuration
│   └── urls.py                # Task URL patterns
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── users/                 # User templates
│   └── tasks/                 # Task templates
├── static/                     # Static files
│   ├── css/                   # Custom CSS
│   └── js/                    # JavaScript files
├── manage.py                   # Django management script
└── README.md                   # This file
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Django_Project
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 👥 Default Users

The system comes with pre-configured users for testing:

### Admin User
- **Username**: admin
- **Password**: admin123
- **Role**: Admin
- **Access**: Full system access

### Manager User
- **Username**: manager
- **Password**: manager123
- **Role**: Manager
- **Access**: Task management and assignment

### Employee User
- **Username**: employee
- **Password**: employee123
- **Role**: Employee
- **Access**: View and update assigned tasks

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Database Configuration
The system uses SQLite by default. To use PostgreSQL or MySQL, update the database settings in `task_management_system/settings.py`.

## 📱 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration

### Users
- `GET /api/users/` - List users (Admin only)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user (Admin only)

### Tasks
- `GET /api/tasks/` - List tasks
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Get task details
- `PUT /api/tasks/{id}/` - Update task
- `DELETE /api/tasks/{id}/` - Delete task
- `PATCH /api/tasks/{id}/update_status/` - Update task status

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category (Admin only)

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Update Bootstrap theme variables
- Customize color schemes and layouts

### Templates
- Edit HTML templates in the `templates/` directory
- Modify base template for global changes
- Customize individual page templates

### Models
- Add new fields to models in `models.py`
- Create new models for additional functionality
- Modify existing model methods

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Test Specific App
```bash
python manage.py test users
python manage.py test tasks
```

## 📊 Database Schema

### Users Table
- Custom user model extending Django's AbstractUser
- Role-based permissions
- Profile information (phone, department, profile picture)

### Tasks Table
- Task details (title, description, priority, status)
- Assignment and ownership
- Time tracking and due dates
- Category and tags

### Categories Table
- Task categories with color coding
- Description and metadata

### Comments Table
- Task comments with author information
- Timestamps and content

### Attachments Table
- File attachments for tasks
- Upload tracking and metadata

## 🔒 Security Features

- **Authentication**: Django's secure authentication system
- **Authorization**: Role-based access control
- **CSRF Protection**: Built-in CSRF token validation
- **SQL Injection Protection**: Django ORM protection
- **XSS Protection**: Template auto-escaping
- **File Upload Security**: File type and size validation

## 🚀 Deployment

### Production Settings
1. Set `DEBUG = False`
2. Configure production database
3. Set up static file serving
4. Configure email settings
5. Set secure `SECRET_KEY`

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 📈 Performance Optimization

- Database query optimization
- Caching strategies
- Static file compression
- Database indexing
- Lazy loading for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🎯 Future Enhancements

- **Real-time Updates**: WebSocket integration
- **Mobile App**: React Native or Flutter app
- **Advanced Analytics**: Task performance metrics
- **Integration**: Third-party service integration
- **Multi-tenancy**: Support for multiple organizations
- **Advanced Reporting**: Custom report generation
- **Workflow Automation**: Automated task routing
- **Time Tracking**: Advanced time tracking features

## ✨ Conclusion

This Task Management System provides a robust, scalable solution for managing tasks and projects with role-based permissions. Built with Django best practices, it offers a modern user interface and comprehensive functionality for teams of all sizes.

The system is production-ready and can be easily customized and extended to meet specific business requirements. 