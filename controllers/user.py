# controllers/user.py
from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models.models import db, Quiz, Question, Score, Subject, Chapter
from sqlalchemy import desc

user = Blueprint('user', __name__)

@user.route('/')
@user.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
        
    # Get available quizzes
    available_quizzes = Quiz.query.filter(
        Quiz.date_of_quiz >= datetime.utcnow().date()
    ).order_by(Quiz.date_of_quiz).all()
    
    # Get user's past attempts
    past_attempts = Score.query.filter_by(
        user_id=current_user.id
    ).order_by(desc(Score.time_stamp_of_attempt)).all()
    
    # Get subjects for filtering
    subjects = Subject.query.all()
    
    return render_template('user/dashboard.html',
                         available_quizzes=available_quizzes,
                         past_attempts=past_attempts,
                         subjects=subjects)

@user.route('/quiz/<int:quiz_id>')
@login_required
def start_quiz(quiz_id):
    if current_user.is_admin:
        flash('Administrators cannot take quizzes.', 'warning')
        return redirect(url_for('admin.dashboard'))
        
    quiz = Quiz.query.get_or_404(quiz_id)
    
    # Check if quiz date is valid
    if quiz.date_of_quiz > datetime.utcnow().date():
        flash('This quiz is not yet available.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    # Check if user has already attempted this quiz
    existing_attempt = Score.query.filter_by(
        user_id=current_user.id,
        quiz_id=quiz_id
    ).first()
    
    if existing_attempt:
        flash('You have already attempted this quiz.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    if not questions:
        flash('No questions available for this quiz.', 'warning')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/quiz.html',
                         quiz=quiz,
                         questions=questions,
                         duration_seconds=int(quiz.time_duration.total_seconds()))

@user.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
        
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    # Calculate score
    total_questions = len(questions)
    correct_answers = 0
    
    for question in questions:
        selected_option = request.form.get(f'question_{question.id}')
        if selected_option and int(selected_option) == question.correct_option:
            correct_answers += 1
    
    score_percentage = (correct_answers / total_questions) * 100
    
    # Save score
    score = Score(
        quiz_id=quiz_id,
        user_id=current_user.id,
        total_scored=score_percentage
    )
    db.session.add(score)
    db.session.commit()
    
    flash(f'Quiz submitted successfully! Your score: {score_percentage:.2f}%', 'success')
    return redirect(url_for('user.view_result', score_id=score.id))

@user.route('/result/<int:score_id>')
@login_required
def view_result(score_id):
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
        
    score = Score.query.get_or_404(score_id)
    if score.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('user.dashboard'))
    
    return render_template('user/result.html', score=score)

@user.route('/subjects/<int:subject_id>/chapters')
@login_required
def get_subject_chapters(subject_id):
    chapters = Chapter.query.filter_by(subject_id=subject_id).all()
    return jsonify([{'id': c.id, 'name': c.name} for c in chapters])

@user.route('/api/user/performance')
@login_required
def get_performance_data():
    scores = Score.query.filter_by(user_id=current_user.id).all()
    data = [{
        'quiz': score.quiz.chapter.name,
        'score': score.total_scored,
        'date': score.time_stamp_of_attempt.strftime('%Y-%m-%d')
    } for score in scores]
    return jsonify(data)