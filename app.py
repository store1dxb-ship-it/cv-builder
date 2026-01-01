import streamlit as st
from fpdf import FPDF

# ===== Step 1: Page Config & Custom Styling =====
st.set_page_config(page_title="Pro CV Builder", layout="centered")

# Professional CSS for a better look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #004d99;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0066cc;
        border: none;
    }
    h1 {
        color: #004d99;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💼 Professional CV Designer")

# Session State track karne ke liye
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

# --- Helper Functions ---
def has_content(val):
    return val and val.strip()

# Professional PDF Generator with Colors
def generate_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    
    # Blue Color Header
    pdf.set_fill_color(0, 77, 153) # Dark Blue
    pdf.rect(0, 0, 210, 40, 'F')
    
    # Name on Blue Background
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 20, data['name'].upper(), ln=True, align='C')
    
    # Contact Details on Blue Background
    pdf.set_font("Arial", '', 10)
    contact = []
    if has_content(data['email']): contact.append(data['email'])
    if has_content(data['phone']): contact.append(data['phone'])
    if has_content(data['address']): contact.append(data['address'])
    pdf.cell(0, 5, " | ".join(contact), ln=True, align='C')
    pdf.ln(15)

    # Body Content
    pdf.set_text_color(0, 0, 0) # Back to Black
    
    sections = [
        ("PROFESSIONAL SUMMARY", data.get('summary')),
        ("EXPERIENCE", data.get('experience')),
        ("EDUCATION", data.get('education')),
        ("PROJECTS", data.get('projects')),
        ("SKILLS", data.get('skills')),
        ("CERTIFICATIONS", data.get('certifications')),
        ("LANGUAGES", data.get('languages'))
    ]
    
    for title, content in sections:
        if has_content(content):
            # Section Heading with Blue underline
            pdf.set_font("Arial", 'B', 12)
            pdf.set_text_color(0, 77, 153)
            pdf.cell(0, 10, title, ln=True)
            pdf.set_draw_color(0, 77, 153)
            pdf.line(10, pdf.get_y(), 60, pdf.get_y())
            pdf.ln(2)
            
            # Content
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", '', 11)
            pdf.multi_cell(0, 6, content)
            pdf.ln(5)
            
    return pdf.output(dest='S').encode('latin-1')

# ===== Step 2: Input Flow =====

# Step logic (Personal -> Links -> Education -> Additional)
if st.session_state.step == 1:
    st.subheader("📍 Personal Information")
    st.session_state.user_data['name'] = st.text_input("Full Name", value=st.session_state.user_data.get('name', ''))
    st.session_state.user_data['email'] = st.text_input("Email Address", value=st.session_state.user_data.get('email', ''))
    st.session_state.user_data['phone'] = st.text_input("Phone Number", value=st.session_state.user_data.get('phone', ''))
    st.session_state.user_data['address'] = st.text_input("Location (City, Country)", value=st.session_state.user_data.get('address', ''))
    if st.button("Save & Next →"):
        if st.session_state.user_data['name']:
            st.session_state.step = 2
            st.rerun()
        else: st.error("Name is required!")

elif st.session_state.step == 2:
    st.subheader("🔗 Links & Summary")
    st.session_state.user_data['linkedin'] = st.text_input("LinkedIn Profile", value=st.session_state.user_data.get('linkedin', ''))
    st.session_state.user_data['summary'] = st.text_area("Summary (Intro)", value=st.session_state.user_data.get('summary', ''), height=150)
    col1, col2 = st.columns(2)
    if col1.button("← Back"): st.session_state.step = 1; st.rerun()
    if col2.button("Next →"): st.session_state.step = 3; st.rerun()

elif st.session_state.step == 3:
    st.subheader("🎓 Background")
    st.session_state.user_data['experience'] = st.text_area("Experience", value=st.session_state.user_data.get('experience', ''), placeholder="Role | Company | Date\nDescribe your tasks...")
    st.session_state.user_data['education'] = st.text_area("Education", value=st.session_state.user_data.get('education', ''), placeholder="Degree | University | Year")
    col1, col2 = st.columns(2)
    if col1.button("← Back"): st.session_state.step = 2; st.rerun()
    if col2.button("Next →"): st.session_state.step = 4; st.rerun()

elif st.session_state.step == 4:
    st.subheader("🚀 Skills & More")
    st.session_state.user_data['projects'] = st.text_area("Projects", value=st.session_state.user_data.get('projects', ''))
    st.session_state.user_data['skills'] = st.text_area("Skills", value=st.session_state.user_data.get('skills', ''))
    st.session_state.user_data['certifications'] = st.text_area("Certifications", value=st.session_state.user_data.get('certifications', ''))
    st.session_state.user_data['languages'] = st.text_input("Languages", value=st.session_state.user_data.get('languages', ''))
    col1, col2 = st.columns(2)
    if col1.button("← Back"): st.session_state.step = 3; st.rerun()
    if col2.button("Finish ✨"): st.session_state.step = 5; st.rerun()

elif st.session_state.step == 5:
    st.success("🎉 Your details are saved!")
    d = st.session_state.user_data
    
    # Preview
    with st.container():
        st.info(f"Reviewing CV for **{d['name']}**")
        if st.button("Edit Again"):
            st.session_state.step = 1
            st.rerun()
            
    # PDF Download
    pdf_bytes = generate_pdf(d)
    st.download_button(
        label="📥 DOWNLOAD PROFESSIONAL PDF",
        data=pdf_bytes,
        file_name=f"{d['name']}_CV.pdf",
        mime="application/pdf",
        use_container_width=True
        )
    
