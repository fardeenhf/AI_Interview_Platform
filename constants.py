# Skill database and question templates
SKILL_DATABASE = {
    "programming_languages": [
        "python", "java", "javascript", "typescript", "c++", "c#", "php", "ruby",
        "go", "rust", "kotlin", "swift", "scala", "perl", "r", "matlab"
    ],
    "web_technologies": [
        "html", "css", "sass", "less", "bootstrap", "tailwind", "jquery",
        "node.js", "express", "react", "angular", "vue", "svelte", "next.js", "nuxt.js"
    ],
    "frameworks": [
        "flask", "django", "fastapi", "spring", "spring boot", "hibernate",
        "asp.net", "asp.net core", "laravel", "rails", "symfony", "codeigniter"
    ],
    "databases": [
        "sql", "mysql", "postgresql", "sqlite", "mongodb", "redis", "elasticsearch",
        "dynamodb", "cassandra", "oracle", "mariadb", "firebase", "sqlalchemy"
    ],
    "data_science_ml": [
        "machine learning", "deep learning", "artificial intelligence", "ai", "data science",
        "pandas", "numpy", "scipy", "scikit-learn", "sklearn", "tensorflow", "pytorch",
        "keras", "matplotlib", "seaborn", "plotly", "jupyter", "nlp", "computer vision",
        "opencv", "statistics", "data analysis", "data mining", "big data"
    ],
    "cloud_devops": [
        "aws", "amazon web services", "azure", "google cloud", "gcp", "docker",
        "kubernetes", "jenkins", "gitlab ci", "github actions", "terraform",
        "ansible", "linux", "bash", "shell scripting", "git", "svn"
    ],
    "tools_technologies": [
        "rest api", "graphql", "microservices", "soap", "webhooks", "oauth", "jwt",
        "linux", "windows", "macos", "agile", "scrum", "kanban", "jira", "confluence"
    ]
}

QUESTION_TEMPLATES = {
    "python": [
        "Explain the difference between lists and tuples in Python.",
        "How does Python's garbage collection work?",
        "What are Python decorators and how do you use them?",
        "Explain the concept of list comprehensions in Python.",
        "How do you handle exceptions in Python?"
    ],
    "java": [
        "Explain the difference between JDK, JRE, and JVM.",
        "What are the main principles of Object-Oriented Programming in Java?",
        "How does garbage collection work in Java?",
        "Explain the difference between ArrayList and LinkedList."
    ],
    "javascript": [
        "Explain the difference between var, let, and const in JavaScript.",
        "How does JavaScript's event loop work?",
        "What are closures in JavaScript and how do they work?",
        "Explain the concept of promises and async/await."
    ],
    "flask": [
        "How does Flask handle routing?",
        "Explain Flask's request-response cycle.",
        "How do you implement authentication in Flask?",
        "What are Flask blueprints and when would you use them?"
    ],
    "django": [
        "Explain Django's MTV (Model-Template-View) architecture.",
        "How does Django handle database migrations?",
        "What are Django models and how do they work?"
    ],
    "react": [
        "Explain the component lifecycle in React.",
        "How does state management work in React?",
        "What are React hooks and how do you use them?"
    ],
    "machine learning": [
        "Explain the bias-variance tradeoff in machine learning.",
        "What is overfitting and how do you prevent it?",
        "Explain the difference between supervised and unsupervised learning."
    ],
    "data science": [
        "Explain the difference between data science and data analytics.",
        "How do you approach a new data science project?",
        "What are the main steps in the data science process?"
    ],
    "sql": [
        "Explain the difference between INNER JOIN and LEFT JOIN.",
        "How do you optimize SQL query performance?",
        "What are database indexes and when should you use them?"
    ],
    "docker": [
        "What are Docker containers and how do they differ from virtual machines?",
        "Explain Docker's architecture and main components.",
        "How do you create and manage Docker images?"
    ],
    "aws": [
        "Explain the difference between EC2, Lambda, and ECS.",
        "How do you implement auto-scaling in AWS?",
        "What are AWS S3 and when would you use it?"
    ],
    "general": [
        "Tell me about a challenging project you worked on and how you overcame difficulties.",
        "How do you stay updated with the latest technology trends?",
        "Describe a situation where you had to learn a new technology quickly.",
        "How do you handle conflicting priorities and deadlines?"
    ]
}

ANSWER_KEYWORDS = {
    "Explain the difference between lists and tuples in Python.": ["lists", "tuples"],
    "How does Python's garbage collection work?": ["reference counting", "garbage collector"],
    "What are Python decorators and how do you use them?": ["decorator", "function"],
    "Explain the concept of list comprehensions in Python.": ["list comprehension"],
    "How do you handle exceptions in Python?": ["try", "except"],
}

SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "PHP", "Ruby",
        "Go", "Rust", "Kotlin", "Swift", "Scala", "Perl", "R", "MATLAB"
    ],
    "Web Technologies": [
        "HTML", "CSS", "SASS", "LESS", "Bootstrap", "Tailwind CSS", "jQuery",
        "Node.js", "Express", "React", "Angular", "Vue.js", "Svelte", "Next.js", "Nuxt.js"
    ],
    "Frameworks": [
        "Flask", "Django", "FastAPI", "Spring", "Spring Boot", "Hibernate",
        "ASP.NET", "ASP.NET Core", "Laravel", "Rails", "Symfony", "CodeIgniter"
    ],
    "Databases": [
        "SQL", "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Elasticsearch",
        "DynamoDB", "Cassandra", "Oracle", "MariaDB", "Firebase", "SQLAlchemy"
    ],
    "Data Science & ML": [
        "Machine Learning", "Deep Learning", "Artificial Intelligence", "Data Science",
        "Pandas", "NumPy", "SciPy", "Scikit-learn", "TensorFlow", "PyTorch",
        "Keras", "Matplotlib", "Seaborn", "Plotly", "Jupyter", "NLP", "Computer Vision",
        "OpenCV", "Statistics", "Data Analysis", "Data Mining", "Big Data"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes", "Jenkins",
        "GitLab CI", "GitHub Actions", "Terraform", "Ansible", "Linux", "Bash",
        "Shell Scripting", "Git", "SVN"
    ],
    "Tools & Technologies": [
        "REST API", "GraphQL", "Microservices", "SOAP", "Webhooks", "OAuth", "JWT",
        "Linux", "Windows", "macOS", "Agile", "Scrum", "Kanban", "Jira", "Confluence"
    ]
}