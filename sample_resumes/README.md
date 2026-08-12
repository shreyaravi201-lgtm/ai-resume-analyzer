# Sample Resumes

This folder contains synthetic, pre-compiled resumes representing three different profiles for system testing and demonstration:

1. **Data Analyst (`data_analyst_resume.docx`)**: Focuses on SQL, Pandas, Excel, Power BI, and Python.
2. **Machine Learning Engineer (`ml_engineer_resume.pdf`)**: Focuses on Scikit-learn, FastAPI, Docker, and MLflow.
3. **NLP Engineer (`nlp_engineer_resume.pdf`)**: Focuses on NLP, Transformers, Hugging Face, and PyTorch.

## How to generate these resumes:
To compile the mock files, run the creation script in your environment:
```powershell
python sample_resumes/create_samples.py
```
This script programmatically builds the Word and PDF documents using python-docx and ReportLab, ensuring a self-contained environment.
