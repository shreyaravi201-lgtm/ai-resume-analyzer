from typing import List, Dict

# Topic-to-weekly-activity map for skill development
SKILL_ROADMAP_MAPPING = {
    # Programming
    "python": "Master Python programming concepts: decorators, generators, multi-threading, and object-oriented programming.",
    "java": "Learn Core Java: syntax, OOP principles, multi-threading, collections framework, and JVM memory management.",
    "c": "Understand C programming: memory allocation, pointers, structures, and low-level system interactions.",
    "c++": "Learn C++ object-oriented features, templates, standard template library (STL), and memory management.",
    "c#": "Study C# and .NET core fundamentals: asynchronous programming, LINQ queries, and building console apps.",
    "javascript": "Understand modern JavaScript (ES6+): closures, asynchronous execution, promises, and DOM manipulation.",
    "typescript": "Learn TypeScript: type annotations, interfaces, generics, and compiling for web applications.",

    # Web
    "html": "Learn HTML5 semantics: layout, forms, accessibility, and modern web standards.",
    "css": "Understand CSS3: flexbox, CSS grid, responsive design, media queries, and animations.",
    "react": "Build single page applications with React: components, state hooks, effect hooks, and context API.",
    "angular": "Understand Angular architecture: modules, components, services, dependency injection, and routing.",
    "node.js": "Develop REST APIs with Node.js and Express: middleware, event-loop, file handling, and routing.",
    "fastapi": "Create modern web APIs with FastAPI: dependency injection, Pydantic validation, and async endpoints.",
    "flask": "Build lightweight backend applications with Flask: routes, templates, and database integrations.",
    "django": "Develop robust backend services with Django: ORM, admin panel, authentication, and REST framework.",

    # Database
    "sql": "Write SQL queries: relational schema design, indexing, joins, aggregation, and window functions.",
    "mysql": "Learn MySQL database management: transactions, query optimizations, and administration.",
    "postgresql": "Understand PostgreSQL: advanced indexing, JSON data types, views, and database optimization.",
    "mongodb": "Learn NoSQL database concepts with MongoDB: documents, collections, and aggregation pipelines.",
    "sqlite": "Use SQLite for lightweight local data storage and application state synchronization.",
    "redis": "Implement caching and in-memory key-value storage using Redis data structures.",

    # Data
    "pandas": "Perform data analysis with Pandas: dataframes, cleaning, filtering, grouping, and merging data.",
    "numpy": "Learn NumPy numerical calculations: multidimensional arrays, vectorization, and linear algebra operations.",
    "excel": "Master Microsoft Excel: advanced formulas (VLOOKUP, INDEX-MATCH), pivot tables, and data modeling.",
    "power bi": "Design business dashboards in Power BI: DAX queries, data relationships, and interactive reporting.",
    "tableau": "Create interactive dashboards in Tableau: data blending, calculated fields, and storytelling.",

    # Machine Learning
    "machine learning": "Understand machine learning algorithms: regression, classification, clustering, and evaluation metrics.",
    "deep learning": "Build deep learning networks: activation functions, backpropagation, and feedforward architectures.",
    "scikit-learn": "Build ML pipelines with Scikit-learn: cross-validation, feature scaling, and hyperparameter tuning.",
    "tensorflow": "Design deep neural networks in TensorFlow and Keras: custom layers, training loops, and TensorBoard.",
    "pytorch": "Develop deep learning architectures in PyTorch: autograd, modules, datasets, and GPU acceleration.",
    "xgboost": "Apply ensemble modeling with XGBoost: gradient boosting, tree pruning, and model optimization.",

    # AI / NLP
    "nlp": "Learn Natural Language Processing: tokenization, stem/lemmatize, TF-IDF, word embeddings, and text classification.",
    "transformers": "Understand Transformer architecture: self-attention mechanisms, encoder-decoders, and BERT/GPT models.",
    "hugging face": "Build NLP pipelines with Hugging Face: pre-trained tokenizers, model hub, and fine-tuning transformers.",
    "llm": "Understand Large Language Models: prompt engineering, context windows, API integrations, and fine-tuning.",
    "rag": "Implement Retrieval-Augmented Generation: vector databases, document chunking, and embedding lookups.",
    "langchain": "Orchestrate agentic workflows in LangChain: memory, chains, agents, and custom tools.",

    # Computer Vision
    "opencv": "Perform image processing in OpenCV: edge detection, contours, blurring, and color spaces.",
    "cnn": "Build Convolutional Neural Networks (CNNs): pooling layers, convolutions, and transfer learning for CV.",
    "yolo": "Implement real-time object detection with YOLO: training custom datasets and inference optimization.",

    # DevOps/Cloud
    "aws": "Learn Cloud architecture on AWS: EC2 instances, S3 storage, IAM roles, and RDS deployment.",
    "azure": "Understand Microsoft Azure cloud services: App Services, SQL Database, and resource groups.",
    "gcp": "Deploy apps on GCP: App Engine, Cloud Storage, Google Kubernetes Engine, and BigQuery.",
    "docker": "Containerize applications with Docker: writing Dockerfiles, docker-compose, and building images.",
    "kubernetes": "Manage container orchestration in Kubernetes: pods, service configuration, and deployments.",
    "git": "Learn version control with Git: commits, branching, merging, rebasing, and resolving conflicts.",
    "github": "Master collaborative coding with GitHub: pull requests, review workflows, and GitHub Actions CI/CD.",
    "ci/cd": "Build continuous integration and deployment pipelines using GitHub Actions, GitLab CI, or Jenkins.",
    "mlflow": "Implement MLOps with MLflow: experiment tracking, model registry, and artifact version control."
}

def generate_roadmap(missing_skills: List[str]) -> List[Dict[str, str]]:
    """
    Generates a weekly learning roadmap based on missing required skills.
    Maps skills to concrete topics and provides a default fallback for missing matches.
    """
    roadmap = []
    if not missing_skills:
        return [
            {
                "week": "Week 1",
                "topic": "Continuous Enhancement",
                "activity": "You match all required skills for this role! Focus on building advanced projects and learning secondary tools."
            }
        ]
        
    for i, skill in enumerate(missing_skills):
        week_num = i + 1
        skill_lower = skill.lower()
        
        # Check if we have a pre-defined learning topic
        if skill_lower in SKILL_ROADMAP_MAPPING:
            activity = SKILL_ROADMAP_MAPPING[skill_lower]
        else:
            activity = f"Master {skill} by reviewing official documentation, completing online tutorials, and building a mini-project."
            
        roadmap.append({
            "week": f"Week {week_num}",
            "topic": f"Learn {skill}",
            "activity": activity
        })
        
    return roadmap
