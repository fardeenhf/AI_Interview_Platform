from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import PyPDF2
import spacy
import os
import logging
import random
from datetime import datetime
from functools import wraps
from constants import SKILL_DATABASE, QUESTION_TEMPLATES, ANSWER_KEYWORDS, SKILL_CATEGORIES

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.error("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    raise

# Configuration
app = Flask(__name__)
app.config.update(
    SECRET_KEY=os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production"),
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database.db')}"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB
    UPLOAD_FOLDER=os.path.join(os.path.dirname(__file__), "uploads")
)

# Create upload folder
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf"}
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    skills = db.Column(db.Text, default="")  # Store skills as comma-separated string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password, password)
    
    def get_skills_list(self):
        """Get skills as a list"""
        if not self.skills:
            return []
        return [skill.strip() for skill in self.skills.split(",") if skill.strip()]
    
    def set_skills_list(self, skills_list):
        """Set skills from a list"""
        self.skills = ",".join(sorted(set(skills_list)))
    
    def __repr__(self):
        return f"<User {self.email}>"


def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")
            
            # Validation
            if not all([name, email, password, confirm_password]):
                flash("All fields are required.", "danger")
                return render_template("register.html")
            
            if len(name) < 2:
                flash("Name must be at least 2 characters.", "danger")
                return render_template("register.html")
            
            if len(password) < 6:
                flash("Password must be at least 6 characters.", "danger")
                return render_template("register.html")
            
            if password != confirm_password:
                flash("Passwords do not match.", "danger")
                return render_template("register.html")
            
            if "@" not in email or "." not in email:
                flash("Invalid email format.", "danger")
                return render_template("register.html")
            
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                flash("Email already registered.", "danger")
                return render_template("register.html")
            
            # Create new user with hashed password
            new_user = User(name=name, email=email)
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"New user registered: {email}")
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Registration error: {str(e)}")
            flash("An error occurred during registration.", "danger")
            return render_template("register.html")
    
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            
            if not email or not password:
                flash("Email and password are required.", "danger")
                return render_template("login.html")
            
            user = User.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                session["user_id"] = user.id
                session["user_name"] = user.name
                session["user_email"] = user.email
                logger.info(f"User logged in: {email}")
                flash(f"Welcome, {user.name}!", "success")
                return redirect(url_for("dashboard"))
            
            logger.warning(f"Failed login attempt for email: {email}")
            flash("Invalid email or password.", "danger")
            return render_template("login.html")
        
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            flash("An error occurred during login.", "danger")
            return render_template("login.html")
    
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    logger.info("User logged out")
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    user = User.query.get(session.get("user_id"))
    return render_template("dashboard.html", user=user)


@app.errorhandler(404)
def not_found_error(error):
    flash("Page not found.", "warning")
    return redirect(url_for("home")), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    logger.error(f"Internal server error: {str(error)}")
    flash("An internal server error occurred.", "danger")
    return redirect(url_for("home")), 500


@app.route("/upload_resume_page")
def upload_resume_page():
    return render_template("upload_resume.html")


def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_skills_from_text(text):
    """Extract skills from resume text"""
    all_skills = {skill for category in SKILL_DATABASE.values() for skill in category}
    text_lower = text.lower()
    found_skills = set()

    # Extract skills by matching
    words = text_lower.split()
    for word in words:
        clean_word = word.strip(".,!?;:()[]{}")
        if clean_word in all_skills:
            found_skills.add(clean_word)

    for skill in all_skills:
        if skill in text_lower:
            found_skills.add(skill)

    # Use spaCy for better context
    try:
        doc = nlp(text)
        for token in doc:
            if token.text.lower() in all_skills:
                found_skills.add(token.text.lower())
    except Exception as e:
        logger.warning(f"spaCy processing failed: {str(e)}")

    return sorted(list(found_skills))


def generate_interview_questions(skills):
    """Generate interview questions based on skills"""
    skill_mapping = {
        "python": "python", "java": "java", "javascript": "javascript",
        "flask": "flask", "django": "django", "react": "react",
        "machine learning": "machine learning", "data science": "data science",
        "sql": "sql", "docker": "docker", "aws": "aws", "azure": "aws"
    }

    categories = {"general"}
    for skill in skills:
        skill_lower = skill.lower()
        if skill_lower in skill_mapping:
            categories.add(skill_mapping[skill_lower])

    questions = []
    for category in categories:
        if category in QUESTION_TEMPLATES:
            questions.extend(QUESTION_TEMPLATES[category][:3])

    random.shuffle(questions)
    return questions[:5]


def evaluate_answer(question, answer):
    """Simple answer evaluation"""
    keywords = ANSWER_KEYWORDS.get(question, [])
    text = answer.lower()
    return any(kw.lower() in text for kw in keywords) if answer else False


def evaluate_answer_detailed(question, answer):
    """
    Detailed answer evaluation with score, feedback, and improvement suggestions
    Returns: (score, feedback, improvement)
    """
    if not answer or not answer.strip():
        return (1, "No answer provided. Please provide a detailed response to demonstrate your understanding.",
                "Try to provide a complete answer that shows your knowledge of the topic.")

    text = answer.lower().strip()
    keywords = ANSWER_KEYWORDS.get(question, [])
    found_keywords = [kw for kw in keywords if kw.lower() in text]

    # Base score calculation
    keyword_score = min(len(found_keywords) / max(len(keywords), 1), 1.0) if keywords else 0.5

    # Length and completeness factors
    word_count = len(text.split())
    length_score = min(word_count / 50, 1.0)  # Expect at least 50 words for completeness

    # Technical accuracy (keyword matching)
    accuracy_score = keyword_score

    # Communication quality (structure, clarity)
    has_structure = any(indicator in text for indicator in ['first', 'then', 'next', 'finally', 'example', 'because', 'therefore'])
    structure_score = 0.8 if has_structure else 0.4

    # Overall score (weighted average)
    overall_score = (accuracy_score * 0.6 + length_score * 0.2 + structure_score * 0.2)
    final_score = max(1, min(10, round(overall_score * 10)))

    # Generate feedback based on performance
    if final_score >= 8:
        feedback = "Excellent answer! You demonstrated strong technical knowledge and clear communication."
    elif final_score >= 6:
        feedback = "Good answer with solid technical content. Your explanation shows understanding of the concepts."
    elif final_score >= 4:
        feedback = "Decent answer, but could be more detailed. You have the right ideas but need more depth."
    else:
        feedback = "Your answer needs more detail and technical accuracy. Focus on the key concepts."

    # Generate improvement suggestions
    improvements = []
    if len(found_keywords) < len(keywords) * 0.7:
        missing_keywords = [kw for kw in keywords if kw.lower() not in text]
        if missing_keywords:
            improvements.append(f"Mention key concepts like: {', '.join(missing_keywords[:3])}")

    if word_count < 30:
        improvements.append("Provide more detailed explanations with examples")

    if not has_structure:
        improvements.append("Structure your answer with clear steps or examples")

    if not improvements:
        improvements.append("Consider adding practical examples or use cases")

    improvement_text = " • ".join(improvements)

    return (final_score, feedback, improvement_text)


def generate_final_evaluation(questions, answers, feedback, scores):
    """Generate comprehensive final evaluation"""
    total_questions = len(questions)
    answered_questions = len([a for a in answers.values() if a.strip()])
    avg_score = sum(scores.values()) / len(scores) if scores else 0

    # Calculate performance metrics
    high_performers = [q for i, q in enumerate(questions) if scores.get(str(i), 0) >= 7]
    low_performers = [q for i, q in enumerate(questions) if scores.get(str(i), 0) < 5]

    # Identify strengths and weaknesses
    strengths = []
    if avg_score >= 7:
        strengths.append("Strong technical knowledge across multiple areas")
    if answered_questions == total_questions:
        strengths.append("Consistent performance and completion rate")
    if any(score >= 8 for score in scores.values()):
        strengths.append("Excellent understanding of advanced concepts")

    areas_for_improvement = []
    if avg_score < 6:
        areas_for_improvement.append("Technical depth and accuracy need improvement")
    if answered_questions < total_questions:
        areas_for_improvement.append("Answer completeness and detail")
    if any(score < 4 for score in scores.values()):
        areas_for_improvement.append("Fundamental concept understanding")

    # Suggest learning topics based on weak areas
    learning_topics = []
    if low_performers:
        # Extract topics from poorly answered questions
        for question in low_performers[:2]:  # Focus on first 2 weak areas
            if "python" in question.lower():
                learning_topics.append("Python fundamentals and best practices")
            elif "javascript" in question.lower():
                learning_topics.append("JavaScript concepts and modern features")
            elif "database" in question.lower() or "sql" in question.lower():
                learning_topics.append("Database design and SQL optimization")
            elif "web" in question.lower():
                learning_topics.append("Web development frameworks and APIs")
            elif "algorithm" in question.lower():
                learning_topics.append("Data structures and algorithms")

    if not learning_topics:
        learning_topics = ["Review core programming concepts", "Practice coding interviews", "Study system design principles"]

    return render_template("interview_simulation.html",
                         questions=questions,
                         answers=answers,
                         feedback=feedback,
                         scores=scores,
                         completed=True,
                         total_questions=total_questions,
                         answered_questions=answered_questions,
                         overall_score=round(avg_score),
                         strengths=strengths,
                         areas_for_improvement=areas_for_improvement,
                         learning_topics=learning_topics)


def get_user_skills():
    """Get user skills from database or session"""
    user = User.query.get(session.get("user_id"))
    return user.get_skills_list() if user else session.get("user_skills", [])


@app.route("/upload_resume", methods=["POST"])
@login_required
def upload_resume():
    try:
        # Check if file is in request
        if "resume" not in request.files:
            flash("No file uploaded.", "danger")
            return redirect(url_for("upload_resume_page"))
        
        file = request.files["resume"]
        
        # Check if file is selected
        if file.filename == "":
            flash("No file selected.", "danger")
            return redirect(url_for("upload_resume_page"))
        
        # Check file extension
        if not allowed_file(file.filename):
            flash("Only PDF files are allowed.", "danger")
            return redirect(url_for("upload_resume_page"))
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        
        # Extract text from PDF
        try:
            pdf_reader = PyPDF2.PdfReader(filepath)
            
            if len(pdf_reader.pages) == 0:
                flash("PDF file is empty.", "danger")
                os.remove(filepath)
                return redirect(url_for("upload_resume_page"))
            
            text = ""
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num}: {str(e)}")
            
            if not text.strip():
                flash("Could not extract text from PDF.", "danger")
                os.remove(filepath)
                return redirect(url_for("upload_resume_page"))
            
            # Extract skills
            skills = extract_skills_from_text(text)
            
            # Save skills to database
            user = User.query.get(session.get("user_id"))
            if user:
                user.set_skills_list(skills)
                db.session.commit()
            
            # Store skills in session for interview questions
            session["user_skills"] = skills
            
            # Clean up
            os.remove(filepath)
            
            logger.info(f"Resume processed for user {session.get('user_id')}: {len(skills)} skills found")
            
            if not skills:
                flash("No skills were automatically detected from your resume. You can manually select your skills below.", "warning")
                return render_template("upload_resume.html", 
                                     skills=[], 
                                     text_preview=text[:500],
                                     show_manual_selection=True)
            else:
                flash(f"Successfully extracted {len(skills)} skills from your resume!", "success")
                return render_template("upload_resume.html", skills=skills, text_preview=text[:500])
        
        except PyPDF2.PdfReadError:
            flash("Invalid or corrupted PDF file.", "danger")
            if os.path.exists(filepath):
                os.remove(filepath)
            return redirect(url_for("upload_resume_page"))
    
    except Exception as e:
        logger.error(f"Resume upload error: {str(e)}")
        flash("An error occurred while processing your resume.", "danger")
        return redirect(url_for("upload_resume_page"))


@app.route("/select_skills", methods=["GET", "POST"])
@login_required
def select_skills():
    user = User.query.get(session.get("user_id"))
    
    if request.method == "POST":
        try:
            # Get selected skills from form
            selected_skills = request.form.getlist("skills")
            
            # Get custom skills
            custom_skills_text = request.form.get("custom_skills", "").strip()
            if custom_skills_text:
                custom_skills = [skill.strip() for skill in custom_skills_text.split(",") if skill.strip()]
                selected_skills.extend(custom_skills)
            
            # Remove duplicates and empty strings
            selected_skills = list(set(skill for skill in selected_skills if skill.strip()))
            
            if not selected_skills:
                flash("Please select at least one skill.", "warning")
                return redirect(url_for("select_skills"))
            
            # Save skills to database
            if user:
                user.set_skills_list(selected_skills)
                db.session.commit()
            
            # Store skills in session for interview questions
            session["user_skills"] = selected_skills
            
            logger.info(f"Skills manually selected for user {session.get('user_id')}: {len(selected_skills)} skills")
            flash(f"Successfully saved {len(selected_skills)} skills!", "success")
            
            # Redirect to interview simulation
            return redirect(url_for("interview_simulation"))
        
        except Exception as e:
            logger.error(f"Skill selection error: {str(e)}")
            flash("An error occurred while saving your skills.", "danger")
            return redirect(url_for("select_skills"))
    
    # GET request - display skill selection form
    # Get user's current skills
    current_skills = user.get_skills_list() if user else []
    
    return render_template("select_skills.html", 
                         skill_categories=SKILL_CATEGORIES, 
                         current_skills=current_skills)


@app.route("/interview_simulation", methods=["GET", "POST"])
@login_required
def interview_simulation():
    user_skills = get_user_skills()
    if not user_skills:
        flash("Please select your skills first to start the interview simulation.", "warning")
        return redirect(url_for("select_skills"))

    # Generate questions if not already in session
    if "simulation_questions" not in session:
        questions = generate_interview_questions(user_skills)
        session["simulation_questions"] = questions
        session["simulation_answers"] = {}
        session["simulation_feedback"] = {}
        session["simulation_scores"] = {}
        session["current_question_index"] = 0
        session["interview_completed"] = False

    questions = session["simulation_questions"]
    current_index = session.get("current_question_index", 0)
    answers = session.get("simulation_answers", {})
    feedback = session.get("simulation_feedback", {})
    scores = session.get("simulation_scores", {})

    # Handle POST request (user submitted an answer)
    if request.method == "POST":
        action = request.form.get("action")
        answer = request.form.get("answer", "").strip()

        # Save the current answer
        if current_index < len(questions):
            answers[str(current_index)] = answer
            session["simulation_answers"] = answers

            # Generate immediate feedback for the current answer
            question = questions[current_index]
            score, feedback_text, improvement = evaluate_answer_detailed(question, answer)

            feedback[str(current_index)] = {
                'score': score,
                'feedback': feedback_text,
                'improvement': improvement
            }
            scores[str(current_index)] = score
            session["simulation_feedback"] = feedback
            session["simulation_scores"] = scores

        if action == "next" and current_index < len(questions) - 1:
            # Move to next question
            session["current_question_index"] = current_index + 1
            return redirect(url_for("interview_simulation"))
        elif action == "previous" and current_index > 0:
            # Move to previous question
            session["current_question_index"] = current_index - 1
            return redirect(url_for("interview_simulation"))
        elif action == "finish" or current_index >= len(questions) - 1:
            # Interview completed
            session["interview_completed"] = True
            session["current_question_index"] = len(questions)  # Mark as completed
            flash("Interview simulation completed! Review your performance below.", "success")
            return redirect(url_for("interview_simulation"))

    # Check if interview is completed
    if session.get("interview_completed", False) or current_index >= len(questions):
        # Show final evaluation
        return generate_final_evaluation(questions, answers, feedback, scores)

    # Show current question with previous feedback if available
    current_question = questions[current_index]
    current_answer = answers.get(str(current_index), "")
    current_feedback = feedback.get(str(current_index))

    return render_template("interview_simulation.html",
                         question=current_question,
                         question_index=current_index,
                         total_questions=len(questions),
                         answer=current_answer,
                         feedback=current_feedback,
                         completed=False)


@app.route("/reset_interview_simulation")
@login_required
def reset_interview_simulation():
    """Reset the interview simulation"""
    session_variables = [
        "simulation_questions", "simulation_answers", "simulation_feedback",
        "simulation_scores", "current_question_index", "interview_completed"
    ]

    for var in session_variables:
        session.pop(var, None)

    flash("Interview simulation has been reset.", "info")
    return redirect(url_for("dashboard"))


@app.route("/voice_interview", methods=["GET", "POST"])
@login_required
def voice_interview():
    user_skills = get_user_skills()
    if not user_skills:
        flash("Please select your skills first to start the voice interview.", "warning")
        return redirect(url_for("select_skills"))
    
    # Generate questions if not already in session
    if "voice_questions" not in session:
        questions = generate_interview_questions(user_skills)
        session["voice_questions"] = questions
        session["voice_answers"] = {}
        session["voice_current_question_index"] = 0
        session["voice_completed"] = False
    
    questions = session["voice_questions"]
    current_index = session.get("voice_current_question_index", 0)
    answers = session.get("voice_answers", {})
    completed = session.get("voice_completed", False)
    
    # Handle POST request (user submitted a voice answer)
    if request.method == "POST":
        action = request.form.get("action")
        answer = request.form.get("answer", "").strip()
        
        # Save the current answer
        if current_index < len(questions):
            answers[str(current_index)] = answer
            session["voice_answers"] = answers
        
        if action == "next" and current_index < len(questions) - 1:
            # Move to next question
            session["voice_current_question_index"] = current_index + 1
            return redirect(url_for("voice_interview"))
        elif action == "previous" and current_index > 0:
            # Move to previous question
            session["voice_current_question_index"] = current_index - 1
            return redirect(url_for("voice_interview"))
        elif action == "finish" or current_index >= len(questions) - 1:
            # Interview completed
            session["voice_completed"] = True
            flash("Voice interview completed! Review your answers below.", "success")
            return redirect(url_for("voice_interview"))
    
    # Check if interview is completed
    if completed or current_index >= len(questions):
        # Show completion summary
        total = len(questions)
        answered = len(answers)
        correct_count = 0
        evaluation = {}
        for idx in range(total):
            ans = answers.get(str(idx), "")
            is_correct = evaluate_answer(questions[idx], ans) if ans else False
            evaluation[str(idx)] = is_correct
            if is_correct:
                correct_count += 1
        rating = round((correct_count / total) * 10) if total > 0 else 0
        return render_template("voice_interview.html", 
                             questions=questions, 
                             answers=answers, 
                             completed=True,
                             total_questions=total,
                             answered_questions=answered,
                             score=rating,
                             correct_count=correct_count,
                             evaluation=evaluation)
    
    # Show current question
    current_question = questions[current_index]
    current_answer = answers.get(str(current_index), "")
    
    return render_template("voice_interview.html", 
                         question=current_question, 
                         question_index=current_index,
                         total_questions=len(questions),
                         answer=current_answer,
                         completed=False)


@app.route("/reset_voice_interview")
@login_required
def reset_voice_interview():
    """Reset the voice interview"""
    if "voice_questions" in session:
        session.pop("voice_questions")
    if "voice_answers" in session:
        session.pop("voice_answers")
    if "voice_current_question_index" in session:
        session.pop("voice_current_question_index")
    if "voice_completed" in session:
        session.pop("voice_completed")
    
    flash("Voice interview has been reset.", "info")
    return redirect(url_for("voice_interview"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        logger.info("Database initialized")
    
    # Set debug based on environment
    debug_mode = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    app.run(debug=debug_mode, host="0.0.0.0", port=5000)    