import streamlit as st
from fpdf import FPDF
import requests

# ==========================================
# 1. AI CONFIGURATION (WORKING KEY & MODEL)
# ==========================================
def get_ai_suggestions(role, info_type):
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg"
    # Using the high-quota model that worked in testing
    model = "gemini-2.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
    
    prompt = f"Write a professional and concise {'resume summary' if info_type == 'summary' else 'job experience bullets'} for a {role}."
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            return res_json['candidates'][0]['content']['parts'][0]['text']
        else:
            return ""
    except:
        return ""

# ==========================================
# 2. PDF GENERATION LOGIC
# ==========================================
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'RESUME', 0, 1, 'C')
        self.ln(5)

def create_pdf(data):
    pdf = PDF()
    pdf.add_page()
    
    # Personal Info
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, data['name'].upper(), ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 7, f"Email: {data['email']} | Phone: {data['phone']}", ln=True)
    pdf.cell(0, 7, f"Role: {data['role']}", ln=True)
    pdf.ln(5)
    
    # Summary
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'PROFESSIONAL SUMMARY', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 7, data['summary'])
    pdf.ln(5)
    
    # Education
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'EDUCATION', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 7, data['education'])
    pdf.ln(5)
    
    # Experience
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'EXPERIENCE', ln=True)
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 7, data['experience'])
    
    return pdf.output(dest='S').encode('latin-1')

# ==========================================
# 3. STREAMLIT UI (MULTI-STEP FORM)
# ==========================================
st.set_page_config(page_title="AI Resume Builder", page_icon="📝")

if 'step' not in st.session_state: st.session_state.step = 1
if 'user_data' not in st.session_state: st.session_state.user_data = {}

st.title("🚀 AI Professional Resume Builder")

# --- STEP 1: Personal Details ---
if st.session_state.step == 1:
    st.header("👤 Step 1: Personal Information")
    with st.form("personal_details"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        role = st.text_input("Target Job Role (e.g. Teacher, Developer)")
        
        if st.form_submit_button("Next ➡️"):
            if name and role:
                st.session_state.user_data.update({"name": name, "email": email, "phone": phone, "role": role})
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please fill Name and Role!")

# --- STEP 2: AI Content Generation ---
elif st.session_state.step == 2:
    st.header("🤖 Step 2: AI Content Generation")
    role = st.session_state.user_data['role']
    
    st.subheader(f"Summary for {role}")
    if st.button("✨ Generate AI Summary"):
        with st.spinner("AI is writing..."):
            suggestion = get_ai_suggestions(role, "summary")
            st.session_state.user_data['summary'] = suggestion

    summary = st.text_area("Edit Summary", value=st.session_state.user_data.get('summary', ''), height=150)
    
    st.divider()
    
    st.subheader("Experience & Education")
    education = st.text_area("Education Details (School, Degree, Year)", placeholder="E.g. Delhi University, B.Ed, 2018")
    experience = st.text_area("Experience Details", placeholder="E.g. 5 Years teaching at ABC School")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Download PDF 📄"):
            st.session_state.user_data.update({"summary": summary, "education": education, "experience": experience})
            pdf_bytes = create_pdf(st.session_state.user_data)
            st.download_button(label="Click here to Download", data=pdf_bytes, file_name="Resume.pdf", mime="application/pdf")

# ==========================================
# 4. REQUIREMENTS.TXT (FOR DEPLOYMENT)
# ==========================================
# requirements.txt mein ye teen lines honi chahiye:
# streamlit
# fpdf
# requests

