# AI Interview Platform

A comprehensive Flask-based web application for resume processing, skill extraction, and interview preparation using AI.

## Features

- **🔐 User Authentication**: Secure registration and login with password hashing
- **📄 Resume Upload**: PDF resume upload and automatic skill extraction
- **🎯 Manual Skill Selection**: Choose skills from organized categories when auto-detection fails
- **🤖 AI-Powered Analysis**: Advanced skill detection using NLP (spaCy)
- **📝 Interview Questions**: Personalized interview questions based on detected skills
- **💾 Skill Persistence**: Save and manage user skills in database
- **🎨 Modern UI**: Beautiful, responsive web interface
- **🛡️ Security**: Password hashing, CSRF protection, and input validation

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2. Run Database Migration
```bash
python migrate_db.py
```

### 3. Start the Application
```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser!

## How It Works

### For New Users:
1. **Register** → Create account with email/password
2. **Login** → Access your dashboard
3. **Upload Resume** → PDF analysis for skill extraction
4. **Manual Selection** → Choose skills if auto-detection fails
5. **Practice** → Get personalized interview questions

### For Existing Users:
1. **Login** → Access dashboard with saved skills
2. **Update Skills** → Modify your skill set anytime
3. **Practice Questions** → Generate new interview questions

## Skill Detection

The platform uses multiple techniques for accurate skill extraction:

- **Text Analysis**: Direct keyword matching
- **NLP Processing**: Context-aware skill detection with spaCy
- **Multi-word Skills**: Recognizes "machine learning", "data science", etc.
- **Fallback Options**: Manual selection when auto-detection fails

### Supported Skill Categories:
- Programming Languages (Python, Java, JavaScript, etc.)
- Web Technologies (HTML, CSS, React, Node.js, etc.)
- Frameworks (Flask, Django, Spring, etc.)
- Databases (SQL, MongoDB, PostgreSQL, etc.)
- Data Science & ML (Pandas, TensorFlow, Scikit-learn, etc.)
- Cloud & DevOps (AWS, Docker, Kubernetes, etc.)
- Other Tools (Agile, Scrum, Jira, etc.)

## Interview Questions

Get personalized interview questions based on your skills:

- **Technical Questions**: Framework-specific, language-specific
- **Behavioral Questions**: General interview preparation
- **Skill-Based**: Questions tailored to your detected competencies
- **Practice Ready**: 10 questions per session with tips

## Project Structure

```
AI_Interview_Platform/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── migrate_db.py          # Database migration script
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── models/               # Data models (future use)
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── upload_resume.html
│   ├── select_skills.html
│   └── interview_questions.html
├── uploads/              # Temporary file storage
└── utils/                # Utility functions
```

## API Endpoints

### Authentication
- `GET /` - Home page (redirects based on login status)
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Dashboard & Skills
- `GET /dashboard` - User dashboard (protected)
- `GET /upload_resume_page` - Resume upload page (protected)
- `POST /upload_resume` - Process resume upload (protected)
- `GET/POST /select_skills` - Manual skill selection (protected)

### Interview Preparation
- `GET /interview_questions` - Generate interview questions (protected)

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    skills TEXT DEFAULT '',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Security Features

- **Password Hashing**: Werkzeug security utilities
- **Session Management**: Secure HTTP-only cookies
- **Input Validation**: Server-side validation
- **File Upload Security**: Type validation, size limits
- **SQL Injection Protection**: SQLAlchemy ORM
- **XSS Protection**: Template escaping

## Troubleshooting

### Resume Upload Issues
- **No skills detected**: Try manual skill selection
- **PDF errors**: Ensure PDF contains selectable text (not just images)
- **Large files**: Maximum 16MB limit

### Skill Detection Problems
- **Missing skills**: Use manual selection to add them
- **Wrong detection**: Update skills through the dashboard
- **Custom skills**: Add via manual selection form

### Database Issues
- **Migration needed**: Run `python migrate_db.py`
- **Permission errors**: Check file permissions
- **Corruption**: Delete database.db and recreate

## Future Enhancements

- [ ] **Skill Analytics**: Progress tracking and recommendations
- [ ] **Question Difficulty**: Easy/Medium/Hard levels
- [ ] **Answer Explanations**: Detailed solutions and tips
- [ ] **Resume Templates**: Generate professional resumes
- [ ] **Interview Simulations**: Timed practice sessions
- [ ] **Progress Tracking**: Learning analytics dashboard
- [ ] **Mobile App**: React Native companion
- [ ] **API Endpoints**: REST API for integrations

## Technology Stack

- **Backend**: Flask 2.3+, SQLAlchemy 2.0+
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **NLP**: spaCy 3.6+ with en_core_web_sm model
- **PDF Processing**: PyPDF2 3.0+
- **Security**: Werkzeug 2.3+

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the logs for error details

---

**Happy Interviewing! 🎯🚀**

## Requirements

- Python 3.8+
- Flask 2.3+
- SQLAlchemy 2.0+
- spaCy 3.6+

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd AI_Interview_Platform
```

### 2. Create virtual environment
```bash
python -m venv .venv
```

### 3. Activate virtual environment

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

### 6. Set up environment variables
```bash
cp .env.example .env
```

Edit `.env` and set your configuration:
```
SECRET_KEY=your-strong-secret-key-here
FLASK_DEBUG=False
DATABASE_URL=sqlite:///database.db
```

### 7. Initialize database
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

## Usage

### Run the application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### Register a new account
1. Click "Register" on the login page
2. Fill in your details with a valid password (min 6 characters)
3. Confirm your password
4. Submit the registration form

### Login
1. Enter your email and password
2. Click "Login"
3. You'll be redirected to your dashboard

### Upload Resume
1. Click "Upload Resume" from the dashboard
2. Select a PDF file from your computer
3. The system will process the PDF and extract skills
4. View the extracted skills on the results page

## Project Structure

```
AI_Interview_Platform/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── database/             # Database files
├── instance/             # Instance folder
├── models/               # Data models
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── upload_resume.html
└── uploads/              # Uploaded resume files (temporary)
```

## Security Features

- **Password Hashing**: Passwords are hashed using Werkzeug's security utilities
- **Session Management**: Secure session handling with httpOnly and SameSite cookies
- **Input Validation**: All user inputs are validated and sanitized
- **File Upload Validation**: Only PDF files are allowed, with size limits
- **Error Handling**: Generic error messages to prevent information leakage
- **Logging**: All important actions are logged for audit trails

## API Endpoints

### Authentication
- `GET /` - Home (redirects to dashboard if logged in, login if not)
- `GET/POST /register` - User registration
- `GET/POST /login` - User login
- `GET /logout` - User logout

### Dashboard
- `GET /dashboard` - User dashboard (protected)

### Resume Processing
- `GET /upload_resume_page` - Resume upload page
- `POST /upload_resume` - Process and upload resume (protected)

## Error Handling

The application includes comprehensive error handling:
- 404 errors redirect to home page
- 500 errors display generic messages
- All exceptions are logged with detailed information
- User-friendly error messages via flash notifications

## Logging

Logs are configured at INFO level and include:
- User registration and login events
- Resume processing details
- Errors and exceptions

## Configuration Management

Configuration can be controlled through:
1. Environment variables (`.env` file)
2. `config.py` for different environments
3. Command-line arguments

### Supported Environments
- `development` - Development with debug mode
- `production` - Production with security enabled
- `testing` - Testing with in-memory database

## Future Enhancements

- [ ] Email verification for registration
- [ ] Password reset functionality
- [ ] Resume storage and history
- [ ] Interview question generation
- [ ] Interview simulations
- [ ] Performance analytics
- [ ] Admin dashboard
- [ ] API rate limiting
- [ ] Multi-language support

## Troubleshooting

### spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### Database locked error
```bash
# Remove the database and reinitialize
rm database.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Port already in use
Change the port in `app.py`:
```python
app.run(debug=debug_mode, host="0.0.0.0", port=5001)
```

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please create an issue in the repository.
