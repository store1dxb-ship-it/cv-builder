import streamlit as st
from fpdf import FPDF
import google.generativeai as genai

# ===== 1. AI Configuration (The Permanent Fix) =====
API_KEY = "AIzaSyBnzIDq_M918jBKRIerScQfOefHDO9J-VM"

# Configure with explicit API version to avoid v1beta 404 error
genai.configure(api_key=API_KEY, transport='rest') 

def get_ai_suggestions(role, info_type="summary"):
    try:
        # Stable model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if info_type == "summary":
            prompt = f"Write a professional 2-line resume summary for a {role}."
        else:
            prompt = f"Write 4 professional bullet points for work experience of a {role} role."
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Agar ye fail hota hai, toh hum 'gemini-pro' try karenge as fallback
        try:
            model_fallback = genai.GenerativeModel('gemini-pro')
            response = model_fallback.generate_content(prompt)
            return response.text
        except:
            return f"AI Error: API limit ya connectivity issue ho sakta hai. Details: {str(e)}"

# ===== 2. Page Styling =====
st.set_page_config(page_title="AI CV Builder", layout="wide")

st.markdown("""
    <style>
    .template-card {
        border: 2px solid #eee;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        background-color: #ffffff;
        margin-bottom: 20px;
    }
    .template-card:hover { border-color: #007bff; transform: scale(1.02); transition: 0.3s; }
    .stButton>button { width: 100%; border-radius: 8px; font-weight: bold; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 1
if 'user_data' not in st.session_state: st.session_state.user_data = {}

# ===== 3. PDF Logic (Templates) =====
def create_pdf(data, style):
    pdf = FPDF()
    pdf.add_page()
    
    if style == "Modern Blue":
        pdf.set_fill_color(0, 77, 153)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 24)
        pdf.set_y(15)
        pdf.cell(0, 10, data['name'].upper(), ln=True, align='C')
    elif style == "Creative Sidebar":
        pdf.set_fill_color(40, 40, 40)
        pdf.rect(0, 0, 65, 297, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 16)
        pdf.set_xy(5, 20)
        pdf.multi_cell(55, 10, data['name'].upper(), align='C')
    elif style == "Elegant Gold":
        pdf.set_draw_color(212, 175, 55)
        pdf.rect(5, 5, 200, 287)
        pdf.set_font("Times", 'B', 24)
        pdf.set_text_color(150, 120, 20)
        pdf.cell(0, 20, data['name'], ln=True, align='C')
    else:
        pdf.set_font("Arial", 'B', 22)
        pdf.cell(0, 15, data['name'], ln=True, align='L')
        pdf.line(10, 25, 200, 25)

    pdf.set_text_color(0, 0, 0)
    pdf.set_y(50 if style != "Creative Sidebar" else 20)
    
    sections = [("Summary", data.get('summary')), ("Experience", data.get('experience')), 
               ("Education", data.get('education')), ("Skills", data.get('skills'))]

    for title, content in sections:
        if content and content.strip():
            if style == "Creative Sidebar": pdf.set_x(70)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, title.upper(), ln=True)
            pdf.set_font("Arial", '', 10)
            if style == "Creative Sidebar": pdf.set_x(70)
            pdf.multi_cell(0, 6, content)
            pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

# ===== 4. UI Flow =====
if st.session_state.step == 1:
    st.title("👤 Step 1: Personal Details")
    st.session_state.user_data['name'] = st.text_input("Full Name", value=st.session_state.user_data.get('name', ''))
    st.session_state.user_data['role'] = st.text_input("Target Job Role (e.g. Data Scientist)", value=st.session_state.user_data.get('role', ''))
    
    if st.button("Next ➡️"):
        if st.session_state.user_data['name'] and st.session_state.user_data['role']:
            st.session_state.step = 2; st.rerun()
        else:
            st.error("Please fill Name and Job Role")

elif st.session_state.step == 2:
    st.title("🤖 Step 2: AI Content")
    role = st.session_state.user_data['role']
    
    if st.button("✨ Generate AI Summary"):
        with st.spinner("Gemini is thinking..."):
            st.session_state.user_data['summary'] = get_ai_suggestions(role, "summary")
    
    summary = st.text_area("Summary", value=st.session_state.user_data.get('summary', ''), height=150)
    
    if st.button("✨ Generate AI Experience"):
        with st.spinner("Gemini is thinking..."):
            st.session_state.user_data['experience'] = get_ai_suggestions(role, "exp")
                
    exp = st.text_area("Experience", value=st.session_state.user_data.get('experience', ''), height=200)
    
    col1, col2 = st.columns(2)
    if col1.button("Back"): st.session_state.step = 1; st.rerun()
    if col2.button("Next"): 
        st.session_state.user_data.update({"summary": summary, "experience": exp})
        st.session_state.step = 3; st.rerun()

elif st.session_state.step == 3:
    st.title("🎓 Step 3: Education & Skills")
    edu = st.text_area("Education", value=st.session_state.user_data.get('education', ''))
    skills = st.text_area("Skills", value=st.session_state.user_data.get('skills', ''))
    col1, col2 = st.columns(2)
    if col1.button("Back"): st.session_state.step = 2; st.rerun()
    if col2.button("Show Templates 🎨"):
        st.session_state.user_data.update({"education": edu, "skills": skills})
        st.session_state.step = 4; st.rerun()

elif st.session_state.step == 4:
    st.title("🎨 Select Template")
    cols = st.columns(3)
    
    template_data = [
        {"name": "Modern Blue", "img": "https://img.freepik.com/free-vector/modern-resume-template_23-2147829285.jpg"},
        {"name": "Classic Black", "img": "https://img.freepik.com/free-vector/professional-resume-template-minimalist-style_23-2148386443.jpg"},
        {"name": "Creative Sidebar", "img": "https://img.freepik.com/free-vector/modern-blue-resume-template_23-2147833008.jpg"},
        {"name": "Elegant Gold", "img": "https://img.freepik.com/free-vector/elegant-cv-template-concept_23-2148398453.jpg"},
        {"name": "Minimalist", "img": "https://img.freepik.com/free-vector/black-white-resume-template_23-2148401344.jpg"}
    ]

    for i, t in enumerate(template_data):
        with cols[i%3]:
            st.markdown('<div class="template-card">', unsafe_allow_html=True)
            st.image(t["img"], use_container_width=True)
            if st.button(f"Select {t['name']}", key=f"btn_{t['name']}"):
                st.session_state.style = t["name"]; st.session_state.step = 5; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.step == 5:
    st.title("✅ Final Step")
    pdf_bytes = create_pdf(st.session_state.user_data, st.session_state.style)
    st.download_button("📥 DOWNLOAD MY CV", data=pdf_bytes, file_name="My_Resume.pdf", use_container_width=True)
    if st.button("Start Again 🔄"):
        st.session_state.step = 1
        st.session_state.user_data = {}
        st.rerun()
        
