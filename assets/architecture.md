# System Architecture

Below is a detailed Mermaid diagram representing the flow of data and modules in the AI Resume Analyzer and Job Recommendation System.

```mermaid
graph TD
    User([User]) -->|Uploads PDF / DOCX| Uploader[Streamlit File Uploader]
    
    subgraph Data Extraction & Preprocessing
        Uploader -->|Bytes stream| Parser{resume_parser.py}
        Parser -->|PDF Text| PyPDF[PyPDF Extraction]
        Parser -->|DOCX Text| DocxExtract[python-docx Extraction]
        
        PyPDF -->|Raw Text| Cleaner{text_cleaner.py}
        DocxExtract -->|Raw Text| Cleaner
        
        Cleaner -->|Redacts PII| PII[Email/Phone Redactor]
        Cleaner -->|Lowercases, normalizes whitespace| CleanText[Cleaned Text]
    end
    
    subgraph Skill Extraction
        CleanText -->|Regex search| Extractor{skill_extractor.py}
        SkillDict[(skill_dictionary.csv)] -->|Load canonicals & aliases| Extractor
        
        Extractor -->|Grouped by category| CategorizedSkills[Categorized Skills]
        Extractor -->|Flat list| FlatSkills[Detected Skills List]
    end
    
    subgraph Matching Engine
        CleanText -->|TF-IDF Vector| Matcher{job_matcher.py}
        FlatSkills -->|Skill overlap| Matcher
        JobDataset[(job_roles.csv)] -->|Job descriptions & required skills| Matcher
        
        Matcher -->|70% Skill Score + 30% Cosine Similarity| Combined[Combined Match Score]
        Combined -->|Sorted descending| RankedRoles[Ranked Job Recommendations]
    end
    
    subgraph Output & Reports
        RankedRoles -->|Selected Target Role| Target[Target Role Details]
        Target -->|Missing required skills| Roadmap{roadmap_generator.py}
        Roadmap -->|Weekly schedule| OutputUI[Dashboard Render]
        
        CategorizedSkills --> OutputUI
        RankedRoles --> OutputUI
        
        OutputUI -->|Triggers PDF compile| Report{report_generator.py}
        Report -->|Compiles PDF stream| PDFDownload([Downloadable PDF Report])
    end
```

### Module Descriptions

1. **`resume_parser.py`**: Reads binary streams directly in memory. Splits pages and handles document cells or paragraphs cleanly.
2. **`text_cleaner.py`**: Performs character cleaning. It leaves technical symbols untouched (such as `+` in `C++` or `#` in `C#`) and masks contact info fields using pattern replacements.
3. **`skill_extractor.py`**: Runs case-insensitive search queries using positive and negative lookarounds to match only whole words.
4. **`job_matcher.py`**: Calculates keyword coverage and fits a TF-IDF text representation on the resume text and preset job profiles to calculate structural matching scores.
5. **`roadmap_generator.py`**: Produces scheduled tasks dynamically mapped to missing technical requirements.
6. **`report_generator.py`**: Compiles an in-memory binary PDF document utilizing ReportLab's SimpleDocTemplate and flowable elements.
