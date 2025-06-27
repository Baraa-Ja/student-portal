
# Student Course Portal

A Flask + SQL Server web app that lets students:
- Register, login/logout
- View and enroll in courses
- Manage their dashboard
- Switch between dark/light themes
- Uses AJAX for enrollment and course list fetch

## 📦 Requirements
```
pip install -r requirements.txt
```

## ⚙️ Configuration
Make sure SQL Server is running and you created a database:
```sql
CREATE DATABASE student_portal;
```

### Update DB URI in `app.py`
```python
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mssql+pyodbc://sa:sa123456@localhost/student_portal'
    '?driver=ODBC+Driver+17+for+SQL+Server'
)
```

## 🚀 Run the App
```
python app.py
```

## 🔐 Test Login (after seeding or registering):
```
Email: Text123@gmail.com
Password: 123
```

## 📁 Folder Structure
```
student-portal/
├── app.py
├── models.py
├── templates/
├── static/
├── api/
├── ajax/
├── create_tables.sql
├── requirements.txt
├── README.md
```
