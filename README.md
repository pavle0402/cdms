# Clinic-Doctor Management System

A simple clinic-doctor management system designed to help clinics and their administrators track doctors, while enabling doctors to manage their patients effectively. This is the initial version of the system and will be upgraded over time.

## Features

- **Clinic Administration**: Track and manage doctors within the clinic
- **Doctor Portal**: Allow doctors to manage their patient records
- **User Management**: Role-based access for clinic admins and doctors

## Local Development Setup

Follow these straightforward steps to get the application running locally:

### Prerequisites

- Python 3.x
- PostgreSQL database
- Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd clinic-doctor-management
   ```

2. **Database Setup**
   - Install and configure PostgreSQL
   - Create a `.env` file in the project root with your database credentials:
     ```env
     DB_NAME=your_database_name
     DB_USER=your_database_user
     DB_PASSWORD=your_database_password
     DB_HOST=localhost
     DB_PORT=5432
     ```

3. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   ```

4. **Activate Virtual Environment**
   - **Linux/macOS:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```

5. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

6. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create Superuser Account**
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create your administrator account.

8. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

🎉 **You're all set!** The application should now be running at `http://localhost:8000`

## Contributing

This project welcomes improvements and contributions. Feel free to enhance the system in any way you see fit.

## Support

For questions or support, please contact: [pavles2002@gmail.com](mailto:pavles2002@gmail.com)

## Technology Stack

- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Environment**: Python Virtual Environment

---

*Thank you for using the Clinic-Doctor Management System!*
