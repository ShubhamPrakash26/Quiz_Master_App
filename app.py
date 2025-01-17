# app.py
from flask import Flask, render_template
from flask_login import LoginManager
from models.models import db, User
from dotenv import load_dotenv
from controllers.auth import auth
from controllers.admin import admin
from controllers.user import user  # Added user controller
from werkzeug.security import generate_password_hash
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///quiz_master.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)  # Added user blueprint

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
def init_db():
    with app.app_context():
        db.create_all()
        # Check if the admin user exists
        admin = User.query.filter_by(username='admin@quizmaster.com').first()
        if not admin:
            admin = User(
                username='admin@quizmaster.com',
                password=generate_password_hash('admin@123'),
                full_name='Administrator',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            
if __name__ == "__main__":
    init_db()
    port = int(os.getenv("PORT", 5000))  
    app.run(host="0.0.0.0", port=port)
    app.run(debug=True)