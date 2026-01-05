import streamlit as st
from fpdf import FPDF
import requests

# ==========================================
# 1. AI CONFIGURATION (GEMINI 2.5 FLASH-LITE)
# ==========================================
def get_ai_suggestions(role, info_type, skills="", experience=""):
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg"
    model = "gemini-2.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
    
    if info_type == "skills":
        prompt = f"List 10 professional skills for a {role} resume. Only comma separated."
    elif info_type == "summary":
        prompt = f"Write a 3-line powerful professional summary for a {role} resume using these skills: {skills}. Focus on impact and expertise."
    elif info_type == "experience":
        prompt = f"Write 5 professional work history bullet points for a {role} role using these skills: {skills}. Use strong action verbs."
    
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data, timeout=12)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return ""
    return ""

# ==========================================
# 2. PDF GENERATION LOGIC
# ==========================================
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'RESUME', 0, 1, 'C')
        self.ln(5)

    def section_title(self, title):
        self.set_font('Arial', 'B', 11)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 7, title, 0, 1, 'L', fill=True)
        self.ln(2)

    def section_content(self, content):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 5, content)
        self.ln(3)

def create_pdf(data):
    pdf = PDF()
    pdf.add_page()
    
    # Personal Header
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 10, data['name'].upper(), ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 5, f"Email: {data['email']} | Phone: {data['phone']}", ln=True)
    pdf.cell(0, 5, f"Target Role: {data['role']}", ln=True)
    if data.get('portfolio'): pdf.cell(0, 5, f"Portfolio: {data['portfolio']}", ln=True)
    pdf.ln(5)
    
    # Standard Sections
    mapping = [
        ('PROFESSIONAL SUMMARY', 'summary'),
        ('SKILLS', 'skills'),
        ('EXPERIENCE', 'experience'),
        ('EDUCATION', 'education'),
        ('LANGUAGES', 'languages'),
        ('CERTIFICATIONS', 'certifications')
    ]
    
    for title, key in mapping:
        if data.get(key):
            pdf.section_title(title)
            pdf.section_content(data[key])
            
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ==========================================
# 3. STREAMLIT UI
# ==========================================
st.set_page_config(page_title="AI Resume Pro", layout="wide")

if 'step' not in st.session_state: st.session_state.step = 1
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# --- STEP 1: Basic Info ---
if st.session_state.step == 1:
    st.title("👤 Step 1: Profile Details")
    with st.form("basics"):
        name = st.text_input("Full Name")
        role = st.text_input("Job Role You Are Applying For", placeholder="e.g. Sales Manager")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        portfolio = st.text_input("LinkedIn/Portfolio (Optional)")
        if st.form_submit_button("Next: Skills ➡️"):
            if name and role:
                st.session_state.user_data.update({"name": name, "role": role, "email": email, "phone": phone, "portfolio": portfolio})
                st.session_state.step = 2
                st.rerun()
            else: st.error("Name aur Role bharna zaroori hai!")

# --- STEP 2: Skills & AI Summary ---
elif st.session_state.step == 2:
    st.title(f"🛠️ Step 2: Skills & Summary for {st.session_state.user_data['role']}")
    role = st.session_state.user_data['role']
    
    # Skills Section
    st.subheader("Skills")
    if st.button("🔍 Get AI Skill Suggestions"):
        st.session_state.user_data['skills'] = get_ai_suggestions(role, "skills")
    skills = st.text_area("Skills (Comma separated)", value=st.session_state.user_data.get('skills', ''), height=100)

    st.divider()

    # AI Summary Section (Based on Screenshot)
    st.subheader("📄 Professional Summary")
    st.info("AI aapke Skills aur Role ke behalf par summary likhega.")
    if st.button("✨ Generate AI Summary"):
        with st.spinner("Writing professional summary..."):
            st.session_state.user_data['summary'] = get_ai_suggestions(role, "summary", skills)
    
    summary = st.text_area("Edit Summary", value=st.session_state.user_data.get('summary', ''), height=150)

    col1, col2 = st.columns(2)
    if col1.button("⬅️ Back"):
        st.session_state.step = 1
        st.rerun()
    if col2.button("Next: Work Experience ➡️"):
        st.session_state.user_data.update({"skills": skills, "summary": summary})
        st.session_state.step = 3
        st.rerun()

# --- STEP 3: Work History & Finalize ---
elif st.session_state.step == 3:
    st.title("🏢 Step 3: Work Experience & Education")
    role = st.session_state.user_data['role']
    skills = st.session_state.user_data.get('skills', '')

    st.subheader("Work Experience")
    if st.button("✍️ Suggest Work History Points"):
        with st.spinner("Generating points..."):
            st.session_state.user_data['experience'] = get_ai_suggestions(role, "experience", skills)
    
    experience = st.text_area("Experience Details", value=st.session_state.user_data.get('experience', ''), height=200)
    
    education = st.text_area("Education", placeholder="Degree, School, Year")
    
    c1, c2 = st.columns(2)
    languages = c1.text_input("Languages")
    certs = c2.text_input("Certifications")

    st.divider()
    
    if st.button("⬅️ Back"):
        st.session_state.step = 2
        st.rerun()
        
    if st.button("Finish & Download Resume 📥"):
        st.session_state.user_data.update({"experience": experience, "education": education, "languages": languages, "certifications": certs})
        pdf_bytes = create_pdf(st.session_state.user_data)
        st.download_button("Download PDF", data=pdf_bytes, file_name=f"{st.session_state.user_data['name']}_Resume.pdf")
        
