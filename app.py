import streamlit as st
from fpdf import FPDF
import requests

# ==========================================
# 1. AI CONFIGURATION (Gemini 2.5)
# ==========================================
def get_ai_suggestions(role, info_type, skills=""):
    # API Key provided by user for final save
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg"
    model = "gemini-2.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
    
    prompts = {
        "skills": f"List 12 hard and soft professional skills for a {role} resume. Comma separated only.",
        "summary": f"Write a compelling 3-line professional summary for a {role} resume incorporating these skills: {skills}.",
        "experience": f"Write 4 detailed work history bullet points for a {role} role, focusing on metrics and achievements. Use skills: {skills}.",
        "projects": f"Describe 2 key projects for a {role} with outcomes.",
        "achievements": f"List 2 major professional achievements or awards for a {role}."
    }
    
    prompt = prompts.get(info_type, "")
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
    except: 
        return "AI Service Busy. Please type manually."
    return ""

# ==========================================
# 2. PDF GENERATION LOGIC
# ==========================================
class PDF(FPDF):
    def header(self):
        # Header strip
        if hasattr(self, 'r'):
            self.set_fill_color(self.r, self.g, self.b)
            self.rect(0, 0, 210, 25, 'F') # Top colored bar
            self.set_text_color(255, 255, 255)
            self.set_font('Arial', 'B', 22)
            # Name in header (Optional style) or below
            # self.cell(0, 15, 'RESUME', 0, 1, 'C') 
            self.ln(5)

def create_pdf(data):
    pdf = PDF()
    pdf.r, pdf.g, pdf.b = data.get('color_rgb', (0, 0, 0))
    pdf.add_page()
    
    # --- NAME & CONTACT ---
    pdf.set_y(30)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 10, data['name'].upper(), ln=True)
    
    pdf.set_font('Arial', 'B', 14)
    pdf.set_text_color(pdf.r, pdf.g, pdf.b) # Accent Color
    pdf.cell(0, 8, data['role'].upper(), ln=True)
    
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(80, 80, 80)
    contact_line = f"{data['email']} | {data['phone']} | {data['city']}, {data['country']}"
    pdf.cell(0, 8, contact_line, ln=True)
    pdf.ln(5)
    
    # --- SECTIONS ---
    sections = [
        ('PROFESSIONAL SUMMARY', 'summary'),
        ('CORE SKILLS', 'skills'),
        ('PROFESSIONAL EXPERIENCE', 'experience'),
        ('KEY PROJECTS', 'projects'),
        ('EDUCATION', 'education'),
        ('CERTIFICATIONS', 'certs'),
        ('ACHIEVEMENTS', 'achievements')
    ]
    
    for title, key in sections:
        content = data.get(key, '').strip()
        if content:
            # Section Header
            pdf.set_text_color(pdf.r, pdf.g, pdf.b)
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, title, ln=True)
            
            # Line separator
            pdf.set_draw_color(200, 200, 200)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x()+190, pdf.get_y())
            pdf.ln(2)
            
            # Content
            pdf.set_text_color(0, 0, 0)
            pdf.set_font('Arial', '', 10)
            pdf.multi_cell(0, 5, content)
            pdf.ln(5)
            
    return pdf.output(dest='S').encode('latin-1', 'ignore')

# ==========================================
# 3. STREAMLIT UI
# ==========================================
st.set_page_config(page_title="AI Resume Pro", layout="wide", page_icon="📄")

# Initialize Session State
if 'step' not in st.session_state: st.session_state.step = 0
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# --- STEP 0: TEMPLATE SELECTION ---
if st.session_state.step == 0:
    st.markdown("<h1 style='text-align: center; color: #333;'>🚀 Select Your Professional Template</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Choose a style that fits your career path.</p>", unsafe_allow_html=True)
    st.write("") # Spacer

    # --- DEFINING FULL TEMPLATES (Bhara Hua Resume) ---
    templates = [
        {
            "id": 0,
            "name": "Pankaj Kumar", 
            "role": "Senior Project Manager", 
            "temp_type": "Executive Class", 
            "border_style": "border-left: 8px solid", 
            "colors": {"Navy": (0, 32, 96), "Teal": (0, 128, 128), "Charcoal": (50, 50, 50)},
            "summary": "Results-oriented Senior Project Manager with 10+ years of experience leading cross-functional teams in IT and Construction. Expert in Agile/Waterfall methodologies, risk mitigation, and budget management (up to $5M).",
            "skills": "Project Planning, Agile & Scrum, Stakeholder Management, Jira, MS Project, Budgeting, Team Leadership, Risk Management.",
            "exp": "• Senior PM at TechFlow | 2019-Present: Led 15+ major delivery cycles.\n• Project Lead at BuildCorp | 2015-2019: Reduced operational costs by 20%.",
            "projects": "• AI Transformation: Led the migration of legacy systems to Cloud AI.\n• Smart City Pilot: Managed a $2M govt pilot project.",
            "edu": "MBA in Operations - IIM Bangalore | 2015\nB.Tech Civil Engineering - IIT Delhi | 2013",
            "certs": "PMP® Certified, CSM® (Certified Scrum Master), Google Project Management.",
            "achievements": "• Awarded 'Project Manager of the Year' 2022.\n• Delivered the Alpha Project 3 months ahead of schedule."
        },
        {
            "id": 1,
            "name": "Punit Yadav", 
            "role": "Lead Data Scientist", 
            "temp_type": "Modern Tech", 
            "border_style": "border-top: 10px solid", 
            "colors": {"Crimson": (139, 0, 0), "Purple": (128, 0, 128), "Blue": (0, 0, 255)},
            "summary": "Innovative Data Scientist with 6+ years of experience in Machine Learning, NLP, and Predictive Analytics. Passionate about turning raw data into actionable business insights.",
            "skills": "Python, TensorFlow, PyTorch, SQL, Pandas, Scikit-Learn, AWS SageMaker, Tableau, PowerBI, Deep Learning.",
            "exp": "• Lead Data Scientist at DataWiz | 2020-Present: Deployed recommendation engines increasing sales by 15%.\n• Data Analyst at FinTech Solutions | 2017-2020.",
            "projects": "• Churn Prediction Model: Reduced customer churn by 12% using XGBoost.\n• Sentiment Analysis Bot: Automating support tickets.",
            "edu": "M.S. in Data Science - BITS Pilani | 2017\nB.E. Computer Science - Pune University | 2015",
            "certs": "TensorFlow Developer Certificate, AWS Certified Machine Learning Specialty.",
            "achievements": "• Published research paper in IEEE 2021.\n• Kaggle Grandmaster (Top 1%)."
        },
        {
            "id": 2,
            "name": "Rashmi Desai", 
            "role": "Senior UI/UX Designer", 
            "temp_type": "Creative Minimal", 
            "border_style": "border: 2px solid", 
            "colors": {"Black": (0, 0, 0), "HotPink": (255, 20, 147), "Orange": (255, 69, 0)},
            "summary": "Creative UI/UX Designer with a keen eye for aesthetics and user-centric design. 7+ years of experience crafting intuitive digital experiences for mobile and web platforms.",
            "skills": "Figma, Adobe XD, Sketch, User Research, Wireframing, Prototyping, HTML/CSS, Interaction Design.",
            "exp": "• Senior Designer at CreativeBox | 2018-Present: Redesigned core app interface boosting retention by 30%.\n• UI Designer at Webify | 2016-2018.",
            "projects": "• E-Commerce Redesign: Complete overhaul of checkout flow.\n• Banking App: Designed accessible interface for elderly users.",
            "edu": "Master of Design (M.Des) - NID Ahmedabad | 2016\nB.Des Visual Comm - Srishti Institute | 2014",
            "certs": "Google UX Design Professional Certificate, Human-Computer Interaction (HCI).",
            "achievements": "• Winner of Awwwards 'Site of the Day' 2022.\n• Featured in Behance Best UI/UX Gallery."
        }
    ]

    cols = st.columns(3)
    
    # Loop to render templates
    for i, temp in enumerate(templates):
        with cols[i]:
            # Default to first color for preview
            if f"color_choice_{i}" not in st.session_state:
                st.session_state[f"color_choice_{i}"] = list(temp['colors'].values())[0]
            
            current_rgb = st.session_state[f"color_choice_{i}"]
            hex_c = '#%02x%02x%02x' % current_rgb

            # --- HTML PREVIEW (Vertical A4 Layout) ---
            # Added overflow-y: hidden to look like a static page, set Aspect Ratio roughly to A4
            html_box = f"""
                <div style="
                    height: 600px; 
                    background: white; 
                    border-radius: 4px; 
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1); 
                    {temp['border_style']} {hex_c}; 
                    padding: 20px; 
                    font-family: Arial, sans-serif; 
                    text-align: left;
                    overflow: hidden;
                    position: relative;
                ">
                    <div style="font-size: 18px; font-weight: bold; color: #222; text-transform: uppercase;">{temp['name']}</div>
                    <div style="font-size: 12px; font-weight: bold; color: {hex_c}; margin-bottom: 10px;">{temp['role']}</div>
                    
                    <div style="font-size: 9px; color: #555; margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 5px;">
                        {temp['name'].lower().replace(' ','')}@email.com | +91 9876543210 | Mumbai, India
                    </div>

                    <div style="margin-bottom: 8px;">
                        <div style="font-size: 10px; font-weight: bold; color: {hex_c};">PROFESSIONAL SUMMARY</div>
                        <div style="font-size: 8px; color: #444; line-height: 1.2;">{temp['summary']}</div>
                    </div>
                    
                    <div style="margin-bottom: 8px;">
                        <div style="font-size: 10px; font-weight: bold; color: {hex_c};">CORE SKILLS</div>
                        <div style="font-size: 8px; color: #444; line-height: 1.2;">{temp['skills']}</div>
                    </div>
                    
                    <div style="margin-bottom: 8px;">
                        <div style="font-size: 10px; font-weight: bold; color: {hex_c};">EXPERIENCE</div>
                        <div style="font-size: 8px; color: #444; line-height: 1.2;">{temp['exp']}</div>
                    </div>

                    <div style="margin-bottom: 8px;">
                        <div style="font-size: 10px; font-weight: bold; color: {hex_c};">KEY PROJECTS</div>
                        <div style="font-size: 8px; color: #444; line-height: 1.2;">{temp['projects']}</div>
                    </div>
                    
                    <div style="margin-bottom: 8px;">
                        <div style="font-size: 10px; font-weight: bold; color: {hex_c};">EDUCATION</div>
                        <div style="font-size: 8px; color: #444; line-height: 1.2;">{temp['edu']}</div>
                    </div>

                    <div style="font-size: 10px; font-weight: bold; color: {hex_c};">CERTIFICATIONS & AWARDS</div>
                    <div style="font-size: 8px; color: #444; line-height: 1.2;">{temp['certs']}</div>
                </div>
            """
            st.markdown(html_box, unsafe_allow_html=True)
            st.write("") # Gap

            # --- CUSTOM COLOR DOTS (Replaced Radio Text) ---
            # We create columns for dots
            c_cols = st.columns(len(temp['colors']))
            selected_color_val = list(temp['colors'].values())[0] # Default
            
            # Helper to draw dots
            color_keys = list(temp['colors'].keys())
            color_values = list(temp['colors'].values())
            
            # Simple Emoji Selector for "Dots"
            # Since custom CSS buttons are hard in pure Streamlit without rerun issues, we use a simple visual hack
            st.write("**Pick Color:**")
            color_selection = st.radio(
                "Color", 
                options=color_keys,
                key=f"radio_{i}",
                label_visibility="collapsed",
                horizontal=True,
                format_func=lambda x: f"● {x}" # Adds a dot text, but the real color is applied below
            )
            
            # Logic to update the preview color based on selection
            st.session_state[f"color_choice_{i}"] = temp['colors'][color_selection]
            
            # Select Button
            if st.button(f"Select {temp['temp_type']}", key=f"btn_{i}", use_container_width=True, type="primary"):
                st.session_state.user_data['template_id'] = i
                st.session_state.user_data['color_rgb'] = temp['colors'][color_selection]
                # Pre-fill data if user wants to start with dummy data (Optional, keeping it blank for user to fill)
                st.session_state.step = 1
                st.rerun()

# --- STEP 1: USER DETAILS ---
elif st.session_state.step == 1:
    st.header("📝 Step 1: Personal Details")
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            email = st.text_input("Email", placeholder="rahul@example.com")
            city = st.text_input("City", placeholder="New Delhi")
        with col2:
            role = st.text_input("Target Job Role", placeholder="e.g. Project Manager")
            phone = st.text_input("Phone", placeholder="+91 98765 43210")
            country = st.text_input("Country", placeholder="India")
        
        submitted = st.form_submit_button("Next Step ➡️")
        if submitted:
            if name and role:
                st.session_state.user_data.update({
                    "name": name, "email": email, "phone": phone, 
                    "role": role, "city": city, "country": country
                })
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please fill Name and Role.")

# --- STEP 2: AI CONTENT GENERATION ---
elif st.session_state.step == 2:
    st.markdown(f"## 🤖 AI Resume Builder: {st.session_state.user_data['role']}")
    role = st.session_state.user_data['role']
    
    # Layout: 2 Columns
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("1. Skills & Summary")
        if st.button("✨ Generate Skills"):
            with st.spinner("AI is thinking..."):
                st.session_state.user_data['skills'] = get_ai_suggestions(role, "skills")
        skills = st.text_area("Core Skills", value=st.session_state.user_data.get('skills', ''), height=100)
        
        if st.button("✨ Generate Summary"):
            if skills:
                with st.spinner("Writing summary..."):
                    st.session_state.user_data['summary'] = get_ai_suggestions(role, "summary", skills)
            else:
                st.warning("Generate or type skills first.")
        summary = st.text_area("Professional Summary", value=st.session_state.user_data.get('summary', ''), height=120)

        st.subheader("3. Education & Certs")
        edu = st.text_area("Education Details", placeholder="Degree, College, Year", value=st.session_state.user_data.get('education', ''))
        certs = st.text_area("Certifications", placeholder="Cert Name, Issuer", value=st.session_state.user_data.get('certs', ''))

    with c2:
        st.subheader("2. Experience & Projects")
        if st.button("✨ Generate Experience"):
            with st.spinner("Crafting experience..."):
                st.session_state.user_data['experience'] = get_ai_suggestions(role, "experience", skills)
        exp = st.text_area("Work Experience", value=st.session_state.user_data.get('experience', ''), height=200)

        if st.button("✨ Generate Projects"):
            with st.spinner("Brainstorming projects..."):
                st.session_state.user_data['projects'] = get_ai_suggestions(role, "projects")
        projects = st.text_area("Key Projects", value=st.session_state.user_data.get('projects', ''), height=150)
        
        if st.button("✨ Generate Achievements"):
             with st.spinner("Finding achievements..."):
                st.session_state.user_data['achievements'] = get_ai_suggestions(role, "achievements")
        achievements = st.text_area("Achievements", value=st.session_state.user_data.get('achievements', ''), height=100)

    # Save Data
    st.session_state.user_data.update({
        "skills": skills, "summary": summary, "experience": exp, 
        "education": edu, "certs": certs, "projects": projects, "achievements": achievements
    })

    st.divider()
    
    # Generate PDF
    if st.button("✅ Finalize & Download PDF", type="primary", use_container_width=True):
        if not summary or not exp:
            st.warning("Please ensure Summary and Experience are filled!")
        else:
            pdf_data = create_pdf(st.session_state.user_data)
            st.success("Resume Generated Successfully!")
            st.download_button(
                label="📥 Download Resume PDF",
                data=pdf_data,
                file_name=f"{st.session_state.user_data['name']}_Resume.pdf",
                mime="application/pdf"
            )
    
    if st.button("⬅️ Restart"):
        st.session_state.step = 0
        st.rerun()
                    
