from flask import Blueprint, request, jsonify, session
from database import db
from Models import Enrollment, Course

ajax = Blueprint('ajax', __name__)

@ajax.route('/ajax/enroll', methods=['POST'])
def ajax_enroll():
    # Check user logged in by session key 'id'
    if 'id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    data = request.get_json()
    course_id = data.get('course_id')

    # Check if already enrolled
    exists = Enrollment.query.filter_by(student_id=session['id'], course_id=course_id).first()
    if exists:
        return jsonify({'success': False, 'message': 'Already enrolled'})

    # Enroll the user
    enrollment = Enrollment(student_id=session['id'], course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()

    # Get course details to send back
    course = Course.query.get(course_id)
    course_data = {
        'id': course.id,
        'title': course.title,
        'description': course.description
    }

    return jsonify({'success': True, 'course': course_data})
