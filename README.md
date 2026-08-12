# AI Resume Analyzer and Job Recommendation System

An offline-first, Natural Language Processing (NLP) and Machine Learning (ML) system designed for educational career guidance. This application allows users to upload a resume in PDF or DOCX format, analyze skill matches, compare profiles across 10 distinct job roles, identify skill gaps, and generate structured weekly learning roadmaps.

---

## Features

- **Multi-Format Resume Support**: Parses text and tables from both PDF and DOCX files in-memory.
- **Controlled Skill Dictionary**: Categorizes 50+ industry-relevant skills with multi-alias mapping (case-insensitive).
- **Dual Matching Signals**:
  - **Skill Match Score (70% weight)**: Calculated using set intersection of required role skills.
  - **TF-IDF Semantic Score (30% weight)**: Employs Scikit-learn's `TfidfVectorizer` and Cosine Similarity to capture vocabulary match.
- **Interactive Dashboard**: Full Streamlit interface with Plotly visualizations, metric cards, and categorized skill badges.
- **Personalized Roadmap**: Instantly schedules a weekly study curriculum based on missing skills.
- **Report Generation**: Exports findings into a professional multi-page PDF using ReportLab.
- **Privacy-Centric & Responsible AI**:
  - Run completely offline—no internet, API keys, or paid services required.
  - Excludes protected demographic information (names, emails, gender indicators, age) from match computations.
  - Resumes are parsed in-memory and never stored on disk.

---

## Architecture

The system follows a modular architectural pipeline:

```
User (Uploads PDF/DOCX)
  │
  ├──► resume_parser.py ──► text_cleaner.py (Removes PII, normalizes terms)
  │                               │
  │     ┌─────────────────────────┘
  │     ▼
  │  skill_extractor.py ◄── [data/skill_dictionary.csv]
  │     │
  │     ├─► Categorized Skills List
  │     ▼
  │  job_matcher.py     ◄── [data/job_roles.csv]
  │     │
  │     ├─► TF-IDF + Cosine Similarity
  │     ├─► Skill Overlap Calculation
  │     ▼
  │  roadmap_generator.py (Builds weekly schedule)
  │     │
  │     ├─► report_generator.py (Compiles ReportLab PDF)
  │     ▼
  │  app.py (Streamlit Dashboard & Plotly Graphs)
```

---

## Technologies

- **Python 3.11** (recommended)
- **Streamlit**: Dashboard and user interaction
- **Pandas & NumPy**: Data processing and matrix calculations
- **Scikit-learn**: TF-IDF Vectorization and Cosine Similarity
- **PyPDF**: PDF parsing
- **python-docx**: DOCX parsing
- **Plotly**: Data visualization
- **ReportLab**: PDF report generation
- **Pytest**: Unit testing framework

---

## Project Structure

```
ai_resume_analyzer/
├── app.py                      # Main Streamlit dashboard interface
├── config.py                   # Setup configs, weights, and Responsible AI disclaimers
├── resume_parser.py            # PDF/DOCX extractors
├── text_cleaner.py             # Normalization and personal info redaction (PII)
├── skill_extractor.py          # Dictionary loader and case-insensitive regex search
├── job_matcher.py              # Cosine similarity and skill overlap score engine
├── roadmap_generator.py        # Mapping of missing skills to study weeks
├── report_generator.py        # ReportLab PDF publisher
├── utils.py                    # Dataset CSV validators
├── requirements.txt            # Package specifications
├── README.md                   # System documentation
├── .gitignore                  # Git untracked pattern index
├── .env.example                # Sample environment file
│
├── data/
│   ├── job_roles.csv           # Prescribed job roles requirements
│   └── skill_dictionary.csv    # Controlled skill aliases
│
├── sample_resumes/
│   ├── create_samples.py       # Programmatic generator of synthetic test resumes
│   └── README.md               # Summary of mock resumes
│
├── reports/
│   └── .gitkeep                # Output directory marker
│
├── tests/
│   ├── test_resume_parser.py   # Test PDF/DOCX extraction
│   ├── test_text_cleaner.py    # Test cleaning & PII redaction
│   ├── test_skill_extractor.py # Test alias mapping
│   ├── test_job_matcher.py     # Test score math and ranking
│   ├── test_roadmap_generator.py # Test curriculum scheduling
│   └── test_cases.csv          # Matrix of test scenarios
│
└── assets/
    └── architecture.md         # Text-based architecture flow diagram
```

---

## Installation & Windows Setup

Follow these commands to configure the project locally on Windows:

1. **Clone or navigate** to the project directory:
   ```powershell
   cd C:\Users\USER\.gemini\antigravity\scratch\ai_resume_analyzer
   ```

2. **Create a virtual environment**:
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   ```powershell
   venv\Scripts\activate
   ```

4. **Upgrade pip and install requirements**:
   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

---

## How to Use

1. **Launch the Streamlit app**:
   ```powershell
   python -m streamlit run app.py
   ```
2. **Generate Sample Resumes** (optional, for easy testing):
   ```powershell
   python sample_resumes/create_samples.py
   ```
   This will generate three sample resumes (`data_analyst_resume.docx`, `ml_engineer_resume.pdf`, and `nlp_engineer_resume.pdf`) under `sample_resumes/`.
3. Open your browser to the URL displayed in the terminal (typically `http://localhost:8501`).
4. Drag and drop one of the sample resumes into the **Upload Resume** tab and click **Run Resume Analysis**.
5. Navigate through the tabs:
   - Check **Resume Overview** for high-level scoring metrics.
   - Look at **Skills Analysis** to see categorized tools identified.
   - View **Job Recommendations** for ranking bar charts and match logs.
   - Select a target role in **Target Role Analysis** to identify skill gaps and review your step-by-step roadmap.
   - Export your custom roadmap and analysis under **Download Report**.

---

## Matching Algorithm

The scoring engine evaluates resumes against job roles via a transparent dual-signal pipeline:

1. **Skill Matching (70% Weight)**:
   $$\text{Skill Score} = \left( \frac{\text{Detected Required Skills}}{\text{Total Required Skills}} \right) \times 100$$
2. **TF-IDF Cosine Similarity (30% Weight)**:
   - Fits a `TfidfVectorizer` on the corpus of job roles and the cleaned resume text.
   - Employs a custom token pattern (`r"[a-z0-9\+\#\.\-\/]+"`) to prevent stripping key technical letters like `C++`, `C#`, and `.NET`.
   - Calculates the cosine similarity matrix between the resume vector and job role representation vector.
3. **Combined Score**:
   $$\text{Combined Score} = (0.70 \times \text{Skill Score}) + (0.30 \times \text{TF-IDF Score})$$

---

## Responsible AI & Fairness

- **PII Exclusion**: Demographic info like email, telephone, links, and names are redacted on input and are not processed for scoring.
- **Fair Features**: The matching logic is purely deterministic based on skills, projects, certifications, and educational keywords. Factors like gender, age, nationality, or disability are not represented in the CSV dataset.
- **Educational Limits**: Scores do not translate to job search probabilities; they measure vocabulary and skill overlap. Standalone keyword presence does not signify absolute capability.

---

## Limitations

- **Syntactic Parsing**: Heavy reliance on character-level string matches. A candidate who describes "building convolutional layers" might not match the keyword "CNN" if it isn't listed.
- **Layout Robustness**: Highly structured two-column PDF grids might occasionally merge sentences out of reading order.
- **TF-IDF Constraints**: Standard TF-IDF treats words as bags of concepts, lacking context around negative qualifiers (e.g. "no experience in Docker").

---

## Future Improvements

1. **Semantic Embeddings**: Integrate Sentence Transformers (e.g., `all-MiniLM-L6-v2`) locally to compute semantic similarity independent of spelling.
2. **Advanced NLP Parsers**: Leverage spaCy's Named Entity Recognition (NER) to isolate roles, organizations, and school categories dynamically.
3. **Interactive Job Uploads**: Allow users to paste a custom job description and run real-time comparisons instead of pre-configured job roles.
4. **FastAPI & DB Integration**: Wrap the engine in a FastAPI backend with PostgreSQL storage for deployment environments.
