import json
import fitz
import docx
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# Extract PDF Text
# -----------------------------
def extract_pdf_text(filepath):

    text = ""

    pdf = fitz.open(filepath)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


# -----------------------------
# Extract DOCX Text
# -----------------------------
def extract_docx_text(filepath):

    doc = docx.Document(filepath)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text


# -----------------------------
# Extract Resume
# -----------------------------
def extract_resume(filepath):

    extension = filepath.split(".")[-1].lower()

    if extension == "pdf":
        return extract_pdf_text(filepath)

    elif extension == "docx":
        return extract_docx_text(filepath)

    return ""


# -----------------------------
# ATS Analysis
# -----------------------------
def analyze_resume(filepath):

    resume_text = extract_resume(filepath)

    prompt = f"""
You are an ATS Resume Analyzer.

Analyze the following resume.

Resume:

{resume_text}

Return ONLY JSON.

{{
"ats_score":90,
"strengths":[
"Strong Java",
"Projects",
"SQL"
],
"missing_skills":[
"Spring Boot",
"Docker",
"AWS"
],
"suggestions":[
"Add achievements",
"Improve project descriptions",
"Mention internships"
],
"recommended_roles":[
"Java Developer",
"Backend Developer",
"Software Engineer"
]
}}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "")
        text = text.replace("```", "")

    if text.startswith("```"):
        text = text.replace("```", "")

    return json.loads(text)