import streamlit as st
from fpdf import FPDF
import requests

# ==========================================
# 1. AI CONFIGURATION (GEMINI 2.5 FLASH-LITE)
# ==========================================
def get_ai_suggestions(role, info_type, skills=""):
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg"
    model = "gemini-2.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
    
    prompts = {
        "skills": f"List 10 professional skills for a {role} resume. Only comma separated.",
        "summary": f"Write a 3-line professional summary for a {role} resume using skills: {skills}.",
        "experience": f"Write 5 work history bullet points for a {role} role using skills: {skills}."
    }
    
    prompt = prompts.get(info_type, "")
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data, timeout=12)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except: return ""
    return ""

# ==========================================
# 2. PDF GENERATION WITH DYNAMIC COLORS
# ==========================================
class PDF(FPDF):
    def header(self):
        # Header strip with selected color
        self.set_fill_color(self.r, self.g, self.b)
        self.rect(0, 0, 210, 20, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'RESUME', 0, 1, 'C')
        self.ln(10)

def create_pdf(data):
    pdf = PDF()
    # Setting dynamic colors from session state
    pdf.r, pdf.g, pdf.b = data['color_rgb']
    
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    # Personal Info
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 10, data['name'].upper(), ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"{data['email']} | {data['phone']} | {data['city']}, {data['country']}", ln=True)
    pdf.ln(5)
    
    sections = [
        ('PROFESSIONAL SUMMARY', 'summary'),
        ('SKILLS', 'skills'),
        ('WORK HISTORY', 'experience'),
        ('EDUCATION', 'education')
    ]
    
    for title, key in sections:
        if data.get(key):
            # Section Header with selected color
            pdf.set_text_color(pdf.r, pdf.g, pdf.b)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, title, ln=True)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+190, pdf.get_y())
            pdf.ln(2)
            # Content
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 6, data[key])
            pdf.ln(5)
            
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ==========================================
# 3. STREAMLIT UI (TEMPLATES + COLORS)
# ==========================================
st.set_page_config(page_title="AI Resume SaaS", layout="wide")

if 'step' not in st.session_state: st.session_state.step = 0
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# --- STEP 0: TEMPLATE & COLOR SELECTION ---
if st.session_state.step == 0:
    st.title("🎨 Select Design & Color")
    
    # Color Map for Professional Variants
    color_options = {
        "Classic Blue": {"Navy": (0, 32, 96), "Royal": (65, 105, 225), "Sky": (0, 176, 240)},
        "Modern Executive": {"Burgundy": (128, 0, 0), "Forest": (34, 139, 34), "Charcoal": (54, 69, 79)},
        "Minimalist": {"Black": (0, 0, 0), "Slate": (112, 128, 144), "Teal": (0, 128, 128)}
    }

    cols = st.columns(3)
    for i, (temp_name, variants) in enumerate(color_options.items()):
        with cols[i]:
            st.markdown(f"""<div style="padding:20px; border-radius:10px; border:2px solid #ddd; text-align:center;">
                        <h3>{temp_name}</h3></div>""", unsafe_content_with_code=True)
            
            # Sub-color selection for each template
            selected_variant = st.selectbox(f"Choose Color for {temp_name}", list(variants.keys()), key=temp_name)
            
            if st.button(f"Use {temp_name}", key=f"btn_{i}"):
                st.session_state.user_data['template'] = temp_name
                st.session_state.user_data['color_rgb'] = variants[selected_variant]
                st.session_state.step = 1
                st.rerun()

# --- STEP 1: PERSONAL INFO ---
elif st.session_state.step == 1:
    st.header("👤 Personal Details")
    with st.form("personal"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        email = c2.text_input("Email ID")
        phone = c1.text_input("Mobile Number")
        role = c2.text_input("Target Job Role")
        city = c1.text_input("City")
        country = c2.text_input("Country")
        
        if st.form_submit_button("Next ➡️"):
            if name and role:
                st.session_state.user_data.update({"name": name, "email": email, "phone": phone, "role": role, "city": city, "country": country})
                st.session_state.step = 2
                st.rerun()
            else: st.error("Name & Role are required!")

# --- STEP 2: AI CONTENT ---
elif st.session_state.step == 2:
    st.header(f"🤖 Content Generation ({st.session_state.user_data['role']})")
    role = st.session_state.user_data['role']
    
    if st.button("🔍 Get AI Skills"):
        st.session_state.user_data['skills'] = get_ai_suggestions(role, "skills")
    skills = st.text_area("Skills", value=st.session_state.user_data.get('skills', ''))
    
    if st.button("✨ Write AI Summary"):
        st.session_state.user_data['summary'] = get_ai_suggestions(role, "summary", skills)
    summary = st.text_area("Summary", value=st.session_state.user_data.get('summary', ''))
    
    if st.button("✍️ Generate Work History"):
        st.session_state.user_data['experience'] = get_ai_suggestions(role, "experience", skills)
    experience = st.text_area("Experience", value=st.session_state.user_data.get('experience', ''), height=200)

    education = st.text_area("Education")

    if st.button("Download Resume 📥"):
        st.session_state.user_data.update({"skills": skills, "summary": summary, "experience": experience, "education": education})
        pdf_bytes = create_pdf(st.session_state.user_data)
        st.download_button("Click to Download PDF", data=pdf_bytes, file_name="Resume.pdf")
        
