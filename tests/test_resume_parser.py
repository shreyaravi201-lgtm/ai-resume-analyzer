import os
import pytest
from resume_parser import parse_resume
from sample_resumes.create_samples import create_docx_data_analyst, create_pdf_ml_engineer

def test_parse_docx_resume(tmp_path):
    """Verifies that DOCX files can be programmatically created and parsed back."""
    docx_path = os.path.join(tmp_path, "test_analyst.docx")
    create_docx_data_analyst(docx_path)
    
    assert os.path.exists(docx_path)
    
    with open(docx_path, "rb") as f:
        text = parse_resume(f, "test_analyst.docx")
        
    assert "Alex Johnson" in text
    assert "Pandas" in text
    assert "Power BI" in text
    assert "SQL" in text

def test_parse_pdf_resume(tmp_path):
    """Verifies that PDF files can be programmatically created and parsed back."""
    pdf_path = os.path.join(tmp_path, "test_ml.pdf")
    create_pdf_ml_engineer(pdf_path)
    
    assert os.path.exists(pdf_path)
    
    with open(pdf_path, "rb") as f:
        text = parse_resume(f, "test_ml.pdf")
        
    assert "Taylor Vance" in text
    assert "FastAPI" in text
    assert "Docker" in text
    assert "Scikit-learn" in text

def test_unsupported_format():
    """Asserts that unsupported formats raise a ValueError."""
    dummy_file = os.path.join("dummy_path", "resume.txt")
    with pytest.raises(ValueError) as excinfo:
        parse_resume(None, "resume.txt")
    assert "Unsupported file format" in str(excinfo.value)
