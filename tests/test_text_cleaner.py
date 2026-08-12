import pytest
from text_cleaner import clean_text, redact_personal_info, detect_sections

def test_clean_text_normalizes():
    text = "Hello  World!\nThis is a   test. \r\n"
    cleaned = clean_text(text)
    # Checks lowercase, punctuation replacement, whitespace compression, period removal at bounds
    assert "hello world" in cleaned
    assert "this is a test" in cleaned

def test_clean_text_preserves_special_tech():
    text = "I work with C++, C#, .NET, Node.js, and scikit-learn."
    cleaned = clean_text(text)
    assert "c++" in cleaned
    assert "c#" in cleaned
    assert ".net" in cleaned
    assert "node.js" in cleaned
    assert "scikit-learn" in cleaned

def test_redact_personal_info():
    raw_info = "My name is John. Email me at john.doe@email.com or call +1-555-019-2834. Visit my site http://google.com."
    redacted = redact_personal_info(raw_info)
    assert "[EMAIL_REDACTED]" in redacted
    assert "[PHONE_REDACTED]" in redacted
    assert "[URL_REDACTED]" in redacted
    assert "john.doe@email.com" not in redacted
    assert "555-019-2834" not in redacted

def test_detect_sections():
    resume_body = (
        "John Doe\nEmail: contact@doe.com\n\n"
        "Summary\nHighly motivated developer.\n\n"
        "Technical Skills\nPython, SQL, C++\n\n"
        "Education\nB.S. Computer Science"
    )
    sections = detect_sections(resume_body)
    assert "summary" in sections
    assert "skills" in sections
    assert "education" in sections
    assert "highly motivated developer" in sections["summary"].lower()
    assert "python, sql, c++" in sections["skills"].lower()
