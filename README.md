# Quiz Management System

A web application for managing quizzes and users, featuring an admin panel for creating and editing quizzes, viewing user details, and tracking quiz performance.

Deployed Website Link:
https://quizdeck-37ht.onrender.com/

## Features

### Admin Panel
- **Manage Quizzes**:
  - Create, edit, and delete quizzes.
  - Assign quizzes to specific chapters and subjects.
  - Set quiz dates and durations.
  - View the number of questions in each quicz.

- **Manage Users**:
  - View user details, including name, email, qualification, and date of birth.
  - Search users dynamically using a search bar.
  - View quiz history and performance for each user.
  - Delete users if needed.

### User Features
- Take quizzes assigned to them.
- View their performance history and scores.

## Tech Stack

### Frontend
- **HTML/CSS** for structure and styling.
- **Bootstrap** for responsive design and interactive UI components.
- **JavaScript** for dynamic search and modal functionality.

### Backend
- **Flask** as the web framework.
- **Python** for server-side logic.

### Database
- **SQLAlchemy** for managing the database.
- **Relational Database** (e.g., SQLite/PostgreSQL/MySQL) for storing quizzes, users, and scores.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/quiz-management-system.git
   cd quiz-management-system
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Configure your database in the `config.py` file.
   - Initialize the database:
     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

5. Run the application:
   ```bash
   flask run
   ```
   The application will be available at `http://127.0.0.1:5000`.

## Usage

### Admin Panel
1. Navigate to `/admin` to access the admin panel.
2. Use the "Manage Quizzes" page to create and manage quizzes.
3. Use the "Manage Users" page to view and manage user information.

### User Panel
1. Users can log in and view their assigned quizzes.
2. Users can take quizzes and view their scores.

## File Structure

```
quiz_master_23f2002770/
├── .gitignore
├── app.py
├── requirements.txt
├── controllers/
│   ├── admin.py
│   ├── auth.py
│   └── user.py
├── forms/
│   ├── admin_forms.py
│   └── auth_forms.py
├── instance/
│   └── quiz_master.db
├── models/
│   └── models.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
├── templates/
│   ├── base.html
│   ├── admin/
│   │   ├── chapters.html
│   │   ├── dashboard.html
│   │   ├── edit_chapter.html
│   │   ├── edit_question.html
│   │   ├── edit_quiz.html
│   │   ├── questions.html
│   │   ├── quizzes.html
│   │   └── subjects.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── user/
│       ├── dashboard.html
│       ├── quiz.html
│       └── result.html
```

## API Endpoints

### User Management
- **GET** `/admin/api/user/<user_id>`: Fetch details of a specific user.

### Quiz Management
- **POST** `/admin/add_quiz`: Add a new quiz.
- **GET** `/admin/edit_quiz/<quiz_id>`: Edit an existing quiz.
- **GET** `/admin/delete_quiz/<quiz_id>`: Delete a quiz.

## Future Enhancements
- Add role-based access control for users and admins.
- Integrate email notifications for quiz reminders.
- Implement real-time quiz taking with a timer.
- Add data visualization for quiz performance.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments
- **Bootstrap** for the responsive UI design.
- **Flask** for the lightweight web framework.
- **SQLAlchemy** for ORM support.

---
For any questions or suggestions, please contact [Shubham Prakash/prakashshubham26@gmail.com].

