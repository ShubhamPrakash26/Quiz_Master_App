from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, Length

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])

class QuestionForm(FlaskForm):
    question_statement = TextAreaField('Question', validators=[DataRequired()])
    option1 = StringField('Option 1', validators=[DataRequired()])
    option2 = StringField('Option 2', validators=[DataRequired()])
    option3 = StringField('Option 3', validators=[DataRequired()])
    option4 = StringField('Option 4', validators=[DataRequired()])
    correct_option = SelectField('Correct Option', 
                               choices=[(1, 'Option 1'), (2, 'Option 2'), 
                                      (3, 'Option 3'), (4, 'Option 4')],
                               coerce=int,
                               validators=[DataRequired()])

class QuizForm(FlaskForm):
    chapter_id = SelectField('Chapter', coerce=int, validators=[DataRequired()])
    date_of_quiz = DateField('Quiz Date', validators=[DataRequired()])
    duration_hours = IntegerField('Duration (Hours)', default=0)
    duration_minutes = IntegerField('Duration (Minutes)', validators=[DataRequired()])
    remarks = TextAreaField('Remarks')