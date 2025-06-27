from flask import Blueprint, jsonify
from Models import Course

api = Blueprint('api', __name__)

@api.route('/api/courses')
def api_courses():
    courses = Course.query.all()
    return jsonify([
        {
            'id': c.id,
            'title': c.title,
            'description': c.description
        } for c in courses
    ])