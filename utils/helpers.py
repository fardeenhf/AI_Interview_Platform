"""Utility functions for the AI Interview Platform"""

import os
import logging
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.utils import secure_filename

logger = logging.getLogger(__name__)

# Skill database
TECHNICAL_SKILLS = {
    # Programming Languages
    "programming_languages": [
        "python", "java", "javascript", "c++", "c#", "php", "ruby", "go", 
        "rust", "kotlin", "swift", "typescript", "perl", "scala", "r"
    ],
    # Web Frameworks
    "web_frameworks": [
        "flask", "django", "fastapi", "spring", "spring boot", "express",
        "react", "angular", "vue", "svelte", "nextjs", "nuxtjs", "gatsby",
        "rails", "laravel", "asp.net", "asp.net core"
    ],
    # Databases
    "databases": [
        "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", 
        "elasticsearch", "dynamodb", "cassandra", "oracle", "mariadb",
        "firebase", "sqlalchemy", "sequelize"
    ],
    # Data Science
    "data_science": [
        "machine learning", "deep learning", "nlp", "computer vision", "ai",
        "data science", "analytics", "tableau", "powerbi", "matplotlib",
        "seaborn", "plotly", "ggplot", "data mining", "statistical analysis"
    ],
    # Libraries & Tools
    "libraries": [
        "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy",
        "scipy", "sklearn", "nltk", "spacy", "opencv", "pillow", "requests"
    ],
    # Cloud & DevOps
    "cloud_devops": [
        "docker", "kubernetes", "aws", "azure", "gcp", "jenkins", "git",
        "gitlab", "github", "ci/cd", "terraform", "ansible", "prometheus",
        "grafana", "linux", "bash", "shell", "nginx", "apache"
    ],
    # API & Services
    "api_services": [
        "rest api", "graphql", "microservices", "soap", "webhooks",
        "oauth", "jwt", "csrf", "cors"
    ]
}


def flatten_skills():
    """Flatten the skill dictionary into a single set"""
    all_skills = set()
    for category_skills in TECHNICAL_SKILLS.values():
        all_skills.update(category_skills)
    return all_skills


def validate_file_extension(filename, allowed_extensions):
    """
    Validate file extension
    
    Args:
        filename: The filename to validate
        allowed_extensions: Set of allowed extensions
        
    Returns:
        bool: True if valid, False otherwise
    """
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def secure_and_validate_filename(filename, max_length=100):
    """
    Secure and validate filename
    
    Args:
        filename: The filename to secure
        max_length: Maximum length of filename
        
    Returns:
        str: Secured filename or None if invalid
    """
    filename = secure_filename(filename)
    if not filename or len(filename) > max_length:
        return None
    return filename


def create_upload_directory(upload_folder):
    """Create upload directory if it doesn't exist"""
    try:
        os.makedirs(upload_folder, exist_ok=True)
        logger.info(f"Upload directory created/verified: {upload_folder}")
        return True
    except Exception as e:
        logger.error(f"Failed to create upload directory: {str(e)}")
        return False


def clean_extracted_text(text):
    """
    Clean extracted text from PDF
    
    Args:
        text: Raw extracted text
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = " ".join(text.split())
    # Remove special characters but keep alphanumeric and common symbols
    text = "".join(c for c in text if c.isalnum() or c in " .,;:-+/()[]")
    return text


def extract_skills_from_text(text):
    """
    Extract skills from text using keyword matching
    
    Args:
        text: Text to extract skills from
        
    Returns:
        dict: Dictionary of skills by category
    """
    text_lower = text.lower()
    found_skills = {}
    
    for category, skills in TECHNICAL_SKILLS.items():
        found_skills[category] = []
        for skill in skills:
            if skill in text_lower:
                found_skills[category].append(skill)
    
    return {k: v for k, v in found_skills.items() if v}


def get_all_skills_flat():
    """Get all skills as a flat sorted list"""
    return sorted(list(flatten_skills()))


def calculate_skill_match_percentage(extracted_skills, total_possible_skills):
    """
    Calculate skill match percentage
    
    Args:
        extracted_skills: Number of extracted skills
        total_possible_skills: Total possible skills in database
        
    Returns:
        float: Match percentage
    """
    if total_possible_skills == 0:
        return 0.0
    return round((extracted_skills / total_possible_skills) * 100, 2)


def format_skills_for_display(found_skills_dict):
    """
    Format found skills dictionary for display
    
    Args:
        found_skills_dict: Dictionary of skills by category
        
    Returns:
        dict: Formatted dictionary with counts and lists
    """
    formatted = {}
    for category, skills in found_skills_dict.items():
        if skills:
            formatted[category] = {
                "count": len(skills),
                "skills": sorted(list(set(skills)))
            }
    return formatted


class RateLimiter:
    """Simple rate limiter for requests"""
    
    def __init__(self, max_requests=100, window_seconds=3600):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def is_allowed(self, user_id):
        """Check if request is allowed for user"""
        import time
        current_time = time.time()
        
        if user_id not in self.requests:
            self.requests[user_id] = []
        
        # Remove old requests outside the window
        self.requests[user_id] = [
            req_time for req_time in self.requests[user_id]
            if current_time - req_time < self.window_seconds
        ]
        
        if len(self.requests[user_id]) >= self.max_requests:
            return False
        
        self.requests[user_id].append(current_time)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter(max_requests=50, window_seconds=3600)
