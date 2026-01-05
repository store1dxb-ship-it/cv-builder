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
# 2. PDF GENERATION LOGIC
# ==========================================
class PDF(FPDF):
    def header(self):
        if hasattr(self, 'r'):
            self.set_fill_color(self.r, self.g, self.b)
            self.rect(0, 0, 210, 20, 'F')
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 15)
            self.cell(0, 10, 'RESUME', 0, 1, 'C')
            self.ln(10)

def create_pdf(data):
    pdf = PDF()
    pdf.r, pdf.g, pdf.b = data.get('color_rgb', (0, 0, 0))
    pdf.add_page()
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_font('Arial', 'B', 20)
    pdf.cell(0, 10, data['name'].upper(), ln=True)
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 5, f"{data['email']} | {data['phone']} | {data['city']}, {data['country']}", ln=True)
    pdf.ln(5)
    
    sections = [
        ('PROFESSIONAL SUMMARY', 'summary'),
        ('CORE SKILLS', 'skills'),
        ('PROFESSIONAL EXPERIENCE', 'experience'),
        ('EDUCATION', 'education'),
        ('CERTIFICATIONS', 'certs'),
        ('KEY PROJECTS', 'projects'),
        ('ACHIEVEMENTS', 'achievements')
    ]
    for title, key in sections:
        if data.get(key):
            pdf.set_text_color(pdf.r, pdf.g, pdf.b)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, title, ln=True)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+190, pdf.get_y())
            pdf.ln(2)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 6, data[key])
            pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ==========================================
# 3. STREAMLIT UI (FINAL DESIGN)
# ==========================================
st.set_page_config(page_title="AI Resume Pro", layout="wide")

if 'step' not in st.session_state: st.session_state.step = 0
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# --- STEP 0: TEMPLATE SELECTION ---
if st.session_state.step == 0:
    st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>📄 Choose Your Templates</h1>", unsafe_allow_html=True)
    
    templates = [
        {
            "name": "Pankaj Kumar", "role": "Senior Project Manager", "temp_type": "Classic Executive", "border": "border-left: 12px solid", 
            "colors": {"Navy": (0, 32, 96), "Royal": (65, 105, 225), "Ocean": (0, 119, 190)},
            "summary": "Results-driven Project Manager with 8+ years of experience in managing cross-functional teams and budgets up to SAR 5M.",
            "skills": "Project Planning, Agile, Waterfall, Stakeholder Management, Risk Management, Jira, MS Project.",
            "exp": "Senior PM at ABC Solutions | DUBAI. Delivered 95% of projects on time."
        },
        {
            "name": "Punit Yadav", "role": "Senior Data Scientist", "temp_type": "Modern Bold", "border": "border-top: 18px solid", 
            "colors": {"Burgundy": (128, 0, 0), "Rose": (255, 102, 102), "Wine": (102, 0, 0)},
            "summary": "Data Scientist with 5+ years of experience in ML and predictive modeling. Expert in extracting strategic insights from 10M+ records.",
            "skills": "Python, R, SQL, Pandas, Scikit-learn, XGBoost, TensorFlow, Power BI, AWS.",
            "exp": "Senior Data Scientist at ABC Analytics | Riyadh. Improved customer retention by 22%."
        },
        {
            "name": "Rashmi Desai", "role": "Senior UI/UX Designer", "temp_type": "Minimalist", "border": "border: 3px solid", 
            "colors": {"Black": (0, 0, 0), "Slate": (112, 128, 144), "Teal": (0, 128, 128)},
            "summary": "Creative UI/UX Designer with 6+ years of experience designing intuitive digital experiences for web and mobile applications.",
            "skills": "Figma, Adobe XD, User Research, Wireframing, Prototyping, Design Systems, Adobe Suite.",
            "exp": "Senior Designer at Creative Digital Studio | Riyadh. Improved user engagement by 30%."
        }
    ]

    cols = st.columns(3)
    for i, temp in enumerate(templates):
        with cols[i]:
            default_rgb = list(temp['colors'].values())[0]
            hex_c = '#%02x%02x%02x' % default_rgb

            # VERTICAL TEMPLATE PREVIEW
            st.markdown(f"""
                <div style="height: 520px; background: white; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); {temp['border']} {hex_c}; padding: 15px; overflow-y: auto; font-family: sans-serif;">
                    <div style="font-size: 16px; font-weight: bold; color: #222;">{temp['name'].upper()}</div>
                    <div style="font-size: 9px; color: #777; margin-bottom: 10px;">{temp['role']} | {temp['name'].lower().replace(' ','')}@pro.com</div>
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">PROFESSIONAL SUMMARY</div>
                    <div style="font-size: 8px; color: #444; margin-bottom: 8px;">{temp['summary']}</div>
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">EXPERIENCE</div>
                    <div style="font-size: 8px; color: #444; margin-bottom: 8px;">{temp['exp']}</div>
                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">CORE SKILLS</div>
                    <div style="font-size: 8px; color: #444;">{temp['skills']}</div>
                    <div style="margin-top: 15px; font-size: 10px; font-weight: bold; color: {hex_c};">EDUCATION</div>
                    <div style="font-size: 8px; color: #444;">Bachelor's Degree - 2017</div>
                </div>
            """, unsafe_allow_html=True)
            
            st.write("Select Color Dot:")
            # HORIZONTAL DOTS (RADIO)
            choice = st.radio("C", list(temp['colors'].keys()), key=f"c_{i}", horizontal=True, label_visibility="collapsed")
            selected_color = temp['colors'][choice]

            if st.button(f"Use {temp['temp_type']}", key=f"b_{i}", use_container_width=True):
                st.session_state.user_data['template'] = temp['temp_type']
                st.session_state.user_data['color_rgb'] = selected_color
                st.session_state.step = 1
                st.rerun()

# --- STEP 1: PERSONAL INFO ---
elif st.session_state.step == 1:
    st.header("👤 Step 1: Personal Information")
    with st.form("personal"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Full Name")
        email = c2.text_input("Email")
        phone = c1.text_input("Phone")
        role = c2.text_input("Job Role")
        city = c1.text_input("City")
        country = c2.text_input("Country")
        if st.form_submit_button("Next: Content ➡️"):
            if name and role:
                st.session_state.user_data.update({"name": name, "email": email, "phone": phone, "role": role, "city": city, "country": country})
                st.session_state.step = 2
                st.rerun()
            else: st.error("Name aur Role zaruri hai!")

# --- STEP 2: AI CONTENT ---
elif st.session_state.step == 2:
    st.header(f"🤖 AI Builder: {st.session_state.user_data['role']}")
    role = st.session_state.user_data['role']
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 Suggest Skills"):
            st.session_state.user_data['skills'] = get_ai_suggestions(role, "skills")
        skills = st.text_area("Skills", value=st.session_state.user_data.get('skills', ''), height=120)
        
        if st.button("✨ Write Summary"):
            st.session_state.user_data['summary'] = get_ai_suggestions(role, "summary", skills)
        summary = st.text_area("Summary", value=st.session_state.user_data.get('summary', ''), height=120)

    with col2:
        if st.button("✍️ Generate Experience"):
            st.session_state.user_data['experience'] = get_ai_suggestions(role, "experience", skills)
        exp = st.text_area("Experience", value=st.session_state.user_data.get('experience', ''), height=180)
        edu = st.text_area("Education", placeholder="University, Degree, Year")

    st.divider()
    
    st.session_state.user_data.update({"skills": skills, "summary": summary, "experience": exp, "education": edu})
    pdf_bytes = create_pdf(st.session_state.user_data)
    
    # SINGLE BUTTON DOWNLOAD
    st.download_button(
        label="Download My PDF Resume 📥",
        data=pdf_bytes,
        file_name=f"{st.session_state.user_data['name']}_Resume.pdf",
        mime="application/pdf",
        use_container_width=True
    )

