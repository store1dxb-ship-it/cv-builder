import streamlit as st
from fpdf import FPDF
import requests

# ==========================================
# 1. AI CONFIGURATION
# ==========================================
def get_ai_suggestions(role, info_type, skills=""):
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg" # Replace with your key if needed
    model = "gemini-2.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
    
    prompts = {
        "skills": f"List 12 professional skills for a {role} resume. Comma separated.",
        "summary": f"Write a 3-line professional summary for a {role}.",
        "experience": f"Write 4 work history bullet points for a {role}.",
        "projects": f"Describe 2 key projects for a {role}.",
        "achievements": f"List 2 major achievements for a {role}."
    }
    
    prompt = prompts.get(info_type, "")
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data, timeout=5)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except: return "AI unavailable. Please type manually."
    return ""

# ==========================================
# 2. PDF GENERATION
# ==========================================
class PDF(FPDF):
    def header(self):
        # Only draw header on first page or if needed
        pass

def create_pdf(data):
    pdf = PDF()
    pdf.r, pdf.g, pdf.b = data.get('color_rgb', (0, 0, 0))
    pdf.add_page()
    
    # Header Section
    pdf.set_fill_color(255, 255, 255)
    pdf.set_y(15)
    
    # Name & Role
    pdf.set_font('Arial', 'B', 24)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, data['name'].upper(), ln=True)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(pdf.r, pdf.g, pdf.b)
    pdf.cell(0, 8, data['role'], ln=True)
    
    # Contact
    pdf.set_font('Arial', '', 9)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, f"{data['email']} | {data['phone']} | {data['city']}, {data['country']}", ln=True)
    pdf.ln(4)
    
    # Sections
    sections = [
        ('PROFESSIONAL SUMMARY', 'summary'),
        ('CORE SKILLS', 'skills'),
        ('EXPERIENCE', 'experience'),
        ('KEY PROJECTS', 'projects'),
        ('EDUCATION', 'education'),
        ('CERTIFICATIONS', 'certs'),
        ('ACHIEVEMENTS', 'achievements')
    ]
    
    for title, key in sections:
        content = data.get(key, '').strip()
        if content:
            pdf.ln(3)
            # Section Title
            pdf.set_font('Arial', 'B', 11)
            pdf.set_text_color(pdf.r, pdf.g, pdf.b)
            pdf.cell(0, 6, title, ln=True)
            
            # Divider Line
            pdf.set_draw_color(200, 200, 200)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+190, pdf.get_y())
            pdf.ln(2)
            
            # Content
            pdf.set_font('Arial', '', 9)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 5, content)
            
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ==========================================
# 3. STREAMLIT UI (FIXED)
# ==========================================
st.set_page_config(layout="wide", page_title="AI Resume Pro", page_icon="📄")

if 'step' not in st.session_state: st.session_state.step = 0
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# --- STEP 0: TEMPLATES ---
if st.session_state.step == 0:
    st.markdown("<h2 style='text-align: center;'>🚀 Select Your Resume Template</h2>", unsafe_allow_html=True)
    st.write("")

    templates = [
        {
            "id": 0, "name": "Pankaj Kumar", "role": "Senior Project Manager", 
            "colors": {"Navy": (0, 32, 96), "Teal": (0, 128, 128)},
            "border": "border-left: 10px solid",
            "summary": "Results-oriented Senior Project Manager with 10+ years of experience leading cross-functional teams in IT. Expert in Agile/Waterfall and budget management.",
            "skills": "Project Planning, Agile & Scrum, Stakeholder Management, Jira, MS Project, Budgeting, Risk Management.",
            "exp": "• Senior PM at TechFlow | 2019-Present: Led 15+ major delivery cycles.\n• Project Lead at BuildCorp | 2015-2019: Reduced costs by 20%.",
            "projects": "• Smart City Pilot: Managed a $2M govt pilot project.",
            "edu": "B.Tech Civil Engineering - IIT Delhi | 2013",
            "certs": "PMP, CSM, Google Project Management"
        },
        {
            "id": 1, "name": "Punit Yadav", "role": "Lead Data Scientist", 
            "colors": {"Crimson": (139, 0, 0), "Purple": (128, 0, 128)},
            "border": "border-top: 10px solid",
            "summary": "Innovative Data Scientist with 6+ years of experience in Machine Learning and NLP. Passionate about turning raw data into actionable insights.",
            "skills": "Python, TensorFlow, SQL, Pandas, Scikit-Learn, AWS SageMaker, Tableau, PowerBI.",
            "exp": "• Lead Data Scientist at DataWiz | 2020-Present: Deployed AI models increasing sales by 15%.\n• Analyst at FinTech | 2017-2020.",
            "projects": "• Churn Prediction Model: Reduced customer churn by 12%.",
            "edu": "M.S. in Data Science - BITS Pilani | 2017",
            "certs": "TensorFlow Developer, AWS ML Specialty"
        },
        {
            "id": 2, "name": "Rashmi Desai", "role": "Senior UI/UX Designer", 
            "colors": {"Black": (0, 0, 0), "Pink": (255, 20, 147)},
            "border": "border: 2px solid",
            "summary": "Creative UI/UX Designer with 7+ years of experience crafting intuitive digital experiences for mobile and web platforms.",
            "skills": "Figma, Adobe XD, User Research, Wireframing, Prototyping, HTML/CSS.",
            "exp": "• Senior Designer at CreativeBox | 2018-Present: Redesigned app boosting retention by 30%.\n• UI Designer at Webify | 2016-2018.",
            "projects": "• Banking App: Designed accessible interface for elderly users.",
            "edu": "Master of Design (M.Des) - NID Ahmedabad | 2016",
            "certs": "Google UX Design, HCI Certificate"
        }
    ]

    cols = st.columns(3)
    
    for i, temp in enumerate(templates):
        with cols[i]:
            # Color Selection
            if f"c_{i}" not in st.session_state: st.session_state[f"c_{i}"] = list(temp['colors'].values())[0]
            
            # --- FIX: HTML PREVIEW ---
            # Using clean HTML structure with valid CSS for A4 feel
            
            # Convert tuple (0,0,0) to hex string #000000
            current_rgb = st.session_state[f"c_{i}"]
            hex_c = '#%02x%02x%02x' % current_rgb
            
            html_code = f"""
            <div style="
                width: 100%;
                height: 550px;
                background-color: white !important;
                color: #222 !important;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.2);
                font-family: Arial, sans-serif;
                overflow: hidden;
                position: relative;
                {temp['border']} {hex_c};
            ">
                <div style="font-size: 18px; font-weight: bold; text-transform: uppercase; color: #000;">{temp['name']}</div>
                <div style="font-size: 12px; font-weight: bold; color: {hex_c}; margin-bottom: 5px;">{temp['role']}</div>
                
                <div style="font-size: 9px; color: #555; margin-bottom: 12px; border-bottom: 1px solid #ddd; padding-bottom: 5px;">
                    {temp['name'].lower().replace(' ','')}@email.com | +91 9876543210 | Mumbai, India
                </div>

                <div style="margin-bottom: 10px;">
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">PROFESSIONAL SUMMARY</div>
                    <div style="font-size: 8px; color: #333; line-height: 1.3;">{temp['summary']}</div>
                </div>

                <div style="margin-bottom: 10px;">
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">CORE SKILLS</div>
                    <div style="font-size: 8px; color: #333; line-height: 1.3;">{temp['skills']}</div>
                </div>

                <div style="margin-bottom: 10px;">
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">EXPERIENCE</div>
                    <div style="font-size: 8px; color: #333; line-height: 1.3;">{temp['exp']}</div>
                </div>
                
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">KEY PROJECTS</div>
                    <div style="font-size: 8px; color: #333; line-height: 1.3;">{temp['projects']}</div>
                </div>

                <div style="margin-bottom: 10px;">
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">EDUCATION</div>
                    <div style="font-size: 8px; color: #333; line-height: 1.3;">{temp['edu']}</div>
                </div>
            </div>
            """
            st.markdown(html_code, unsafe_allow_html=True)
            
            # Controls below the card
            st.write(f"**Theme:**")
            color_name = st.radio("C", list(temp['colors'].keys()), key=f"r_{i}", horizontal=True, label_visibility="collapsed")
            st.session_state[f"c_{i}"] = temp['colors'][color_name]
            
            if st.button(f"Select {temp['name']}", key=f"b_{i}", use_container_width=True, type="primary"):
                st.session_state.user_data = {
                    "template_id": i,
                    "color_rgb": temp['colors'][color_name],
                    "border_style": temp['border']
                }
                st.session_state.step = 1
                st.rerun()

# --- STEP 1: USER INPUT ---
elif st.session_state.step == 1:
    st.header("📝 Personal Details")
    with st.form("info"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        email = c2.text_input("Email")
        phone = c1.text_input("Phone")
        role = c2.text_input("Job Role")
        city = c1.text_input("City")
        country = c2.text_input("Country")
        if st.form_submit_button("Next ➡️"):
            if name and role:
                st.session_state.user_data.update({"name": name, "email": email, "phone": phone, "role": role, "city": city, "country": country})
                st.session_state.step = 2
                st.rerun()

# --- STEP 2: AI BUILDER ---
elif st.session_state.step == 2:
    st.header(f"🤖 Resume Builder: {st.session_state.user_data.get('role', 'Professional')}")
    role = st.session_state.user_data.get('role', '')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Generate Skills ⚡"):
            st.session_state.user_data['skills'] = get_ai_suggestions(role, "skills")
        skills = st.text_area("Skills", value=st.session_state.user_data.get('skills', ''), height=100)
        
        if st.button("Generate Summary ⚡"):
            st.session_state.user_data['summary'] = get_ai_suggestions(role, "summary", skills)
        summary = st.text_area("Summary", value=st.session_state.user_data.get('summary', ''), height=100)
        
    with col2:
        if st.button("Generate Experience ⚡"):
            st.session_state.user_data['experience'] = get_ai_suggestions(role, "experience", skills)
        exp = st.text_area("Experience", value=st.session_state.user_data.get('experience', ''), height=150)
        
        if st.button("Generate Projects ⚡"):
            st.session_state.user_data['projects'] = get_ai_suggestions(role, "projects")
        pro = st.text_area("Projects", value=st.session_state.user_data.get('projects', ''), height=100)

    # Education & Certs
    c3, c4 = st.columns(2)
    edu = c3.text_input("Education (Degree, College, Year)", value=st.session_state.user_data.get('education', ''))
    certs = c4.text_input("Certifications", value=st.session_state.user_data.get('certs', ''))
    achievements = st.text_input("Achievements", value=st.session_state.user_data.get('achievements', ''))
    
    # Update Data
    st.session_state.user_data.update({
        "skills": skills, "summary": summary, "experience": exp, 
        "projects": pro, "education": edu, "certs": certs, "achievements": achievements
    })
    
    st.divider()
    if st.button("✅ Download PDF Resume", use_container_width=True, type="primary"):
        pdf_bytes = create_pdf(st.session_state.user_data)
        st.download_button("Click to Download 📥", data=pdf_bytes, file_name=f"{st.session_state.user_data.get('name', 'Resume')}.pdf", mime="application/pdf")
        
    if st.button("⬅️ Start Over"):
        st.session_state.step = 0
        st.rerun()

