from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from functools import wraps
from models.models import db, Subject, Chapter, Quiz, Question, User, Score
from forms.admin_forms import SubjectForm, ChapterForm, QuizForm, QuestionForm
from sqlalchemy.orm import joinedload
from models.models import db, User, Subject, Chapter, Quiz, Question, Score

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    subjects_count = Subject.query.count()
    chapters_count = Chapter.query.count()
    quizzes_count = Quiz.query.count()
    users_count = User.query.filter_by(is_admin=False).count()
    
    recent_quizzes = Quiz.query.order_by(Quiz.date_of_quiz.desc()).limit(5).all()
    recent_users = User.query.filter_by(is_admin=False).order_by(User.id.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         subjects_count=subjects_count,
                         chapters_count=chapters_count,
                         quizzes_count=quizzes_count,
                         users_count=users_count,
                         recent_quizzes=recent_quizzes,
                         recent_users=recent_users)

# Subject Management
@admin.route('/admin/subjects', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_subjects():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.name.data, description=form.description.data)
        db.session.add(subject)
        db.session.commit()
        flash('Subject added successfully!', 'success')
        return redirect(url_for('admin.manage_subjects'))
    
    subjects = Subject.query.all()
    return render_template('admin/subjects.html', form=form, subjects=subjects)

@admin.route('/admin/subjects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subject(id):
    subject = Subject.query.get_or_404(id)
    form = SubjectForm(obj=subject)
    
    if form.validate_on_submit():
        try:
            subject.name = form.name.data
            subject.description = form.description.data
            db.session.commit()
            flash('Subject updated successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')
        return redirect(url_for('admin.manage_subjects'))
        
    return render_template('admin/edit_subject.html', form=form, subject=subject)

@admin.route('/admin/subjects/<int:id>/delete')
@login_required
@admin_required
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin.manage_subjects'))

# Chapter Management
@admin.route('/admin/chapters', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_chapters():
    form = ChapterForm()
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
    
    if form.validate_on_submit():
        chapter = Chapter(
            name=form.name.data,
            description=form.description.data,
            subject_id=form.subject_id.data
        )
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter added successfully!', 'success')
        return redirect(url_for('admin.manage_chapters'))
    
    chapters = Chapter.query.all()
    return render_template('admin/chapters.html', form=form, chapters=chapters)

@admin.route('/admin/chapters/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    form = ChapterForm(obj=chapter)
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]

    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        chapter.subject_id = form.subject_id.data
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('admin.manage_chapters'))

    return render_template('admin/edit_chapter.html', form=form, chapter=chapter)

@admin.route('/admin/chapters/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_chapter(id):
    chapter = Chapter.query.get_or_404(id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully!', 'success')
    return redirect(url_for('admin.manage_chapters'))

# Quiz Management
@admin.route('/admin/quizzes')
@login_required
@admin_required
def manage_quizzes():
    form = QuizForm()
    form.chapter_id.choices = [(c.id, f"{c.subject.name} - {c.name}") 
                              for c in Chapter.query.join(Subject).all()]
    
    if form.validate_on_submit():
        duration = timedelta(
            hours=form.duration_hours.data,
            minutes=form.duration_minutes.data
        )
        quiz = Quiz(
            chapter_id=form.chapter_id.data,
            date_of_quiz=form.date_of_quiz.data,
            time_duration=duration,
            remarks=form.remarks.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz added successfully!', 'success')
        return redirect(url_for('admin.manage_quizzes'))
    
    quizzes = Quiz.query.options(joinedload(Quiz.chapter)).all()
    return render_template('admin/quizzes.html', form=form, quizzes=quizzes)

@admin.route('/admin/quizzes/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_quiz():
    form = QuizForm()
    chapters = Chapter.query.all()
    form.chapter_id.choices = [(chapter.id, f"{chapter.subject.name} - {chapter.name}") for chapter in chapters]

    if form.validate_on_submit():
        duration = timedelta(hours=form.duration_hours.data, minutes=form.duration_minutes.data)
        new_quiz = Quiz(
            chapter_id=form.chapter_id.data,
            date_of_quiz=form.date_of_quiz.data,
            time_duration=duration,
            remarks=form.remarks.data
        )
        db.session.add(new_quiz)
        db.session.commit()
        flash('Quiz added successfully!', 'success')
        return redirect(url_for('admin.manage_quizzes'))

    return render_template('admin/quizzes.html', form=form)

@admin.route('/quiz/edit/<int:id>', methods=['GET', 'POST'])
def edit_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    form = QuizForm()

    if form.validate_on_submit():
        quiz.chapter_id = form.chapter_id.data
        quiz.date_of_quiz = form.date_of_quiz.data
        quiz.time_duration = timedelta(hours=form.duration_hours.data, minutes=form.duration_minutes.data)
        quiz.remarks = form.remarks.data
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin.manage_quizzes'))

    # Pre-fill form for GET request
    form.chapter_id.data = quiz.chapter_id
    form.date_of_quiz.data = quiz.date_of_quiz
    form.duration_hours.data = quiz.time_duration.seconds // 3600
    form.duration_minutes.data = (quiz.time_duration.seconds % 3600) // 60
    form.remarks.data = quiz.remarks

    return render_template('admin/edit_quiz.html', form=form, quiz=quiz)

@admin.route('/quiz/delete/<int:id>', methods=['POST', 'GET'])
def delete_quiz(id):
    quiz = Quiz.query.get_or_404(id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin.manage_quizzes'))


# Question Management
@admin.route('/admin/quizzes/<int:quiz_id>/questions', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_questions(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    
    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz_id,
            question_statement=form.question_statement.data,
            option1=form.option1.data,
            option2=form.option2.data,
            option3=form.option3.data,
            option4=form.option4.data,
            correct_option=form.correct_option.data
        )
        db.session.add(question)
        db.session.commit()
        flash('Question added successfully!', 'success')
        return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))
    
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    return render_template('admin/questions.html', 
                         form=form, 
                         questions=questions, 
                         quiz=quiz)

@admin.route('/admin/quizzes/<int:quiz_id>/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_question(quiz_id, question_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)

    if form.validate_on_submit():
        question.question_statement = form.question_statement.data
        question.option1 = form.option1.data
        question.option2 = form.option2.data
        question.option3 = form.option3.data
        question.option4 = form.option4.data
        question.correct_option = form.correct_option.data
        db.session.commit()
        flash('Question updated successfully!', 'success')
        return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))

    return render_template(
        'admin/edit_question.html',
        form=form,
        quiz=quiz,
        question=question
    )

@admin.route('/admin/quizzes/<int:quiz_id>/questions/<int:question_id>/delete', methods=['POST', 'GET'])
@login_required
@admin_required
def delete_question(quiz_id, question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin.manage_questions', quiz_id=quiz_id))


# User Management
@admin.route('/admin/users')
@login_required
@admin_required
def manage_users():
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/users.html', users=users)

# Quiz Results
@admin.route('/admin/results')
@login_required
@admin_required
def view_results():
    scores = Score.query.order_by(Score.time_stamp_of_attempt.desc()).all()
    return render_template('admin/results.html', scores=scores)