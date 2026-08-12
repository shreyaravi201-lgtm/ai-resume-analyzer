import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

from config import (
    SKILL_DICTIONARY_PATH,
    JOB_ROLES_PATH,
    RESPONSIBLE_AI_NOTICE,
    SCORE_EXPLANATION,
    MISSING_SKILL_WARNING,
    PRIVACY_STATEMENT,
    get_match_level
)
from utils import validate_job_roles_csv, validate_skill_dictionary_csv
from resume_parser import parse_resume
from text_cleaner import clean_text, redact_personal_info
from skill_extractor import load_skill_dictionary, extract_skills
from job_matcher import load_job_roles, match_resume_to_roles
from roadmap_generator import generate_roadmap
from report_generator import generate_pdf_report

# Page configurations
st.set_page_config(
    page_title="AI Resume Analyzer & Job Matcher",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Dataset Validations on Load
if not os.path.exists(SKILL_DICTIONARY_PATH) or not os.path.exists(JOB_ROLES_PATH):
    st.error("Error: Dataset files not found. Please ensure job_roles.csv and skill_dictionary.csv are in the data/ folder or at the root level of your repository.")
    st.stop()

valid_roles, roles_msg = validate_job_roles_csv(JOB_ROLES_PATH)
valid_skills, skills_msg = validate_skill_dictionary_csv(SKILL_DICTIONARY_PATH)

if not valid_roles:
    st.error(f"Validation Error in job_roles.csv: {roles_msg}")
    st.stop()
if not valid_skills:
    st.error(f"Validation Error in skill_dictionary.csv: {skills_msg}")
    st.stop()

# 2. Caching Datasets
@st.cache_data
def get_cached_skill_dict():
    return load_skill_dictionary(SKILL_DICTIONARY_PATH)

@st.cache_data
def get_cached_job_roles():
    return load_job_roles(JOB_ROLES_PATH)

skill_dict = get_cached_skill_dict()
job_roles = get_cached_job_roles()

# Initialize session state variables for resume data
if "resume_parsed" not in st.session_state:
    st.session_state.resume_parsed = False
    st.session_state.filename = ""
    st.session_state.char_count = 0
    st.session_state.raw_text = ""
    st.session_state.cleaned_text = ""
    st.session_state.detected_skills = []
    st.session_state.categorized_skills = {}
    st.session_state.role_matches = []

# 3. Sidebar UI
with st.sidebar:
    st.title("💼 AI Career Assistant")
    st.markdown("---")
    st.subheader("About")
    st.info(
        "This tool leverages Natural Language Processing (NLP) and matching algorithms "
        "to compare your resume skills against predefined job roles, identify gaps, "
        "and generate a step-by-step roadmap."
    )
    
    st.subheader("Responsible AI Notice")
    st.warning(RESPONSIBLE_AI_NOTICE)
    
    st.subheader("Privacy Policy")
    st.caption(PRIVACY_STATEMENT)

# 4. Main Page Header
st.title("AI Resume Analyzer & Job Recommendation System")
st.markdown("Analyze your resume, discover suitable roles, identify skill gaps, and build a learning roadmap.")
st.markdown("---")

# 5. Tabbed Interface Setup
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📥 Upload Resume",
    "📊 Resume Overview",
    "🛠️ Skills Analysis",
    "🎯 Job Recommendations",
    "🚀 Target Role Analysis",
    "📄 Download Report"
])

# TAB 1: RESUME UPLOAD
with tab1:
    st.header("Upload Your Resume")
    st.markdown("Supported formats: **PDF** or **DOCX** (Max size: 10MB)")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "docx"],
        help="Upload your professional resume for instant analysis."
    )
    
    if uploaded_file is not None:
        # Validate file size
        file_size_mb = uploaded_file.size / (1024 * 1024)
        if file_size_mb > 10:
            st.error(f"File size exceeds limit of 10MB (Uploaded size: {file_size_mb:.2f}MB). Please upload a smaller file.")
        else:
            if st.button("Run Resume Analysis", type="primary"):
                with st.spinner("Parsing and analyzing resume..."):
                    try:
                        # Parse
                        raw_text = parse_resume(uploaded_file, uploaded_file.name)
                        
                        # Clean & Redact Personal Info
                        cleaned_text = clean_text(raw_text)
                        redacted_raw = redact_personal_info(raw_text)
                        
                        # Extract skills
                        cat_skills, flat_skills = extract_skills(cleaned_text, skill_dict)
                        
                        # Match with Job Roles
                        matches = match_resume_to_roles(cleaned_text, flat_skills, job_roles)
                        
                        # Update session state
                        st.session_state.resume_parsed = True
                        st.session_state.filename = uploaded_file.name
                        st.session_state.char_count = len(raw_text)
                        st.session_state.raw_text = redacted_raw
                        st.session_state.cleaned_text = cleaned_text
                        st.session_state.detected_skills = flat_skills
                        st.session_state.categorized_skills = cat_skills
                        st.session_state.role_matches = matches
                        
                        st.success("Resume analysis completed successfully! Navigate to the next tabs to view findings.")
                    except Exception as e:
                        st.error(f"An error occurred while analyzing the resume. Details: {str(e)}")
    else:
        # Empty State
        st.write("### Welcome! 👋")
        st.markdown(
            "To begin, drag and drop or upload your resume in the section above.\n\n"
            "**What happens next?**\n"
            "1. **Text Extraction**: The system extracts the text contents in-memory.\n"
            "2. **Skill Mapping**: Finds matches from a controlled dictionary of 50+ technical tools and methods.\n"
            "3. **Role Comparison**: Compares the overlap against 10 technical career paths using TF-IDF and Skill matching.\n"
            "4. **Career Roadmap**: Suggests weekly topics based on missing required skills."
        )

# Check if resume is parsed before displaying subsequent tabs
if not st.session_state.resume_parsed:
    for tab in [tab2, tab3, tab4, tab5, tab6]:
        with tab:
            st.warning("Please upload and analyze a resume in the 'Upload Resume' tab first.")
else:
    # TAB 2: OVERVIEW
    with tab2:
        st.header("Resume Overview")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filename", st.session_state.filename)
        with col2:
            st.metric("Character Count", f"{st.session_state.char_count:,}")
        with col3:
            st.metric("Unique Skills Found", len(st.session_state.detected_skills))
            
        top_match = st.session_state.role_matches[0]
        st.markdown("---")
        st.subheader("Key Findings Summary")
        
        m_level = get_match_level(top_match['combined_score'])
        
        col_summary_1, col_summary_2 = st.columns(2)
        with col_summary_1:
            st.markdown(f"### Top Recommended Role: **{top_match['role_name']}**")
            st.markdown(f"**Score:** `{top_match['combined_score']}%` ({m_level})")
            st.markdown(f"**Description:** {top_match['description']}")
        with col_summary_2:
            st.markdown("#### Matched Required Skills")
            if top_match['matched_required_skills']:
                st.write(", ".join(top_match['matched_required_skills']))
            else:
                st.write("None")
                
            st.markdown("#### Missing Required Skills")
            if top_match['missing_required_skills']:
                st.write(", ".join(top_match['missing_required_skills']))
            else:
                st.write("None!")

    # TAB 3: SKILLS ANALYSIS
    with tab3:
        st.header("Detected Technical Skills")
        
        if not st.session_state.detected_skills:
            st.warning(
                "We could not confidently identify technical skills from this resume. "
                "Try uploading a text-based resume or ensure your Skills/Projects/Experience "
                "sections are clearly written."
            )
        else:
            st.markdown("These skills were parsed and categorized based on our controlled vocabulary:")
            
            # Render skills in cards/columns grouped by category
            cats = list(st.session_state.categorized_skills.keys())
            num_cols = min(3, len(cats))
            
            if num_cols > 0:
                cols = st.columns(num_cols)
                for idx, cat in enumerate(cats):
                    col_idx = idx % num_cols
                    with cols[col_idx]:
                        with st.container():
                            st.markdown(f"#### 📁 {cat}")
                            for s in st.session_state.categorized_skills[cat]:
                                st.markdown(f"- {s}")
                            st.write("")

    # TAB 4: JOB RECOMMENDATIONS
    with tab4:
        st.header("Job Role Matches & Recommendations")
        
        # Plotly chart
        df_chart = pd.DataFrame(st.session_state.role_matches)
        
        # Color match levels for readability
        df_chart["Match Rating"] = df_chart["combined_score"].apply(get_match_level)
        
        fig = px.bar(
            df_chart,
            x="combined_score",
            y="role_name",
            orientation="h",
            labels={"combined_score": "Combined Match Score (%)", "role_name": "Job Role"},
            title="Overview of Roles Ranked by Fit",
            color="combined_score",
            color_continuous_scale="Blues",
            range_x=[0, 100]
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=450)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.subheader("Top 3 Career Recommendations")
        
        for idx, rec in enumerate(st.session_state.role_matches[:3], 1):
            with st.expander(f"**#{idx} Recommended: {rec['role_name']}** — Match Score: `{rec['combined_score']}%`"):
                st.write(f"*{rec['description']}*")
                
                col_rec1, col_rec2 = st.columns(2)
                with col_rec1:
                    st.success(f"Matched Required Skills ({len(rec['matched_required_skills'])}):")
                    st.write(", ".join(rec['matched_required_skills']) if rec['matched_required_skills'] else "None")
                with col_rec2:
                    st.error(f"Missing Required Skills ({len(rec['missing_required_skills'])}):")
                    st.write(", ".join(rec['missing_required_skills']) if rec['missing_required_skills'] else "None")

    # TAB 5: TARGET ROLE ANALYSIS
    with tab5:
        st.header("Target Role Analysis & Roadmap")
        
        # Dropdown selection
        role_names_list = [r["role_name"] for r in job_roles]
        
        # Default to the top recommended role
        default_index = role_names_list.index(top_match["role_name"])
        
        target_role_name = st.selectbox(
            "Select Target Role for Detailed Analysis:",
            options=role_names_list,
            index=default_index
        )
        
        # Find target role match record
        target_match = next(r for r in st.session_state.role_matches if r["role_name"] == target_role_name)
        
        # Score metric cards
        col_score1, col_score2, col_score3 = st.columns(3)
        with col_score1:
            st.metric("Combined Score", f"{target_match['combined_score']}%")
        with col_score2:
            st.metric("Skill Overlap Score", f"{target_match['skill_score']}%")
        with col_score3:
            st.metric("TF-IDF Semantic Similarity", f"{target_match['tfidf_score']}%")
            
        with st.expander("ℹ️ How is this score calculated?"):
            st.markdown(SCORE_EXPLANATION)
            
        st.markdown("---")
        
        # Gap analysis
        st.subheader("Skill Gap Analysis")
        st.warning(MISSING_SKILL_WARNING)
        
        col_gap1, col_gap2 = st.columns(2)
        with col_gap1:
            st.markdown("#### ✅ Required Skills Found")
            if target_match["matched_required_skills"]:
                for s in target_match["matched_required_skills"]:
                    st.markdown(f"- {s}")
            else:
                st.write("None detected.")
                
            st.markdown("#### 🌟 Preferred Skills Found")
            if target_match["matched_preferred_skills"]:
                for s in target_match["matched_preferred_skills"]:
                    st.markdown(f"- {s}")
            else:
                st.write("None detected.")
                
        with col_gap2:
            st.markdown("#### ❌ Missing Required Skills")
            if target_match["missing_required_skills"]:
                for s in target_match["missing_required_skills"]:
                    st.markdown(f"- <font color='red'>{s}</font>", unsafe_allow_html=True)
            else:
                st.success("You match all required skills for this role!")
                
            st.markdown("#### 🌠 Missing Preferred Skills")
            if target_match["missing_preferred_skills"]:
                for s in target_match["missing_preferred_skills"]:
                    st.markdown(f"- {s}")
            else:
                st.write("No preferred skills missing.")
                
        st.markdown("---")
        
        # Roadmap Generation
        st.subheader("Personalized Weekly Learning Roadmap")
        st.markdown("A step-by-step curriculum to acquire missing skills:")
        
        roadmap = generate_roadmap(target_match["missing_required_skills"])
        
        for item in roadmap:
            with st.container():
                st.markdown(f"🗓️ **{item['week']}** — **{item['topic']}**")
                st.markdown(item["activity"])
                st.write("")

    # TAB 6: DOWNLOAD REPORT
    with tab6:
        st.header("Download Report")
        st.markdown("Generate and download a comprehensive PDF report summarizing your resume analysis, career matches, skill gaps, and learning roadmaps.")
        
        # Gather inputs for report
        target_role_name_report = st.selectbox(
            "Select Target Role for Report Export:",
            options=role_names_list,
            index=default_index,
            key="report_role_select"
        )
        
        report_target_match = next(r for r in st.session_state.role_matches if r["role_name"] == target_role_name_report)
        report_roadmap = generate_roadmap(report_target_match["missing_required_skills"])
        
        # Build PDF
        try:
            pdf_bytes = generate_pdf_report(
                filename=st.session_state.filename,
                categorized_skills=st.session_state.categorized_skills,
                top_recommendations=st.session_state.role_matches,
                target_role_analysis=report_target_match,
                roadmap=report_roadmap
            )
            
            st.download_button(
                label="📄 Download PDF Analysis Report",
                data=pdf_bytes,
                file_name=f"Resume_Analysis_Report_{target_role_name_report.replace(' ', '_')}.pdf",
                mime="application/pdf",
                type="primary"
            )
        except Exception as e:
            st.error(f"Could not generate PDF report. Error details: {str(e)}")
