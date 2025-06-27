# seed_courses.py
from database import db
from Models import Course
from App import app

with app.app_context():
    if Course.query.count() == 0:
        courses = [
            Course(title="Python Fundamentals", description="Learn the basics of Python."),
            Course(title="Web Development with Flask", description="Build web apps using Flask."),
            Course(title="SQL & Databases", description="Understand relational databases and SQL."),
            Course(title="JavaScript Essentials", description="Start coding dynamic frontends."),
        ]
        db.session.add_all(courses)
        db.session.commit()
        print("Courses seeded successfully.")
    else:
        print("Courses already exist.")
