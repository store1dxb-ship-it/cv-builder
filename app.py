
import streamlit as st
from fpdf import FPDF

# ===== Step 1: UI Styles =====
st.set_page_config(page_title="Professional CV Builder", layout="wide")

st.markdown("""
    <style>
    .template-card {
        border: 2px solid #eee;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        background-color: #ffffff;
    }
    .template-card:hover {
        border-color: #007bff;
        transform: scale(1.02);
        transition: 0.3s;
    }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 1
if 'user_data' not in st.session_state: st.session_state.user_data = {}

def has_content(val):
    return val and str(val).strip()

# ===== Step 2: 5 Template PDF Logic =====
def create_pdf(data, style):
    pdf = FPDF()
    pdf.add_page()
    
    # --- TEMPLATE 1: MODERN BLUE ---
    if style == "Modern Blue":
        pdf.set_fill_color(0, 77, 153)
        pdf.rect(0, 0, 210, 40, 'F')
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 24)
        pdf.set_y(15)
        pdf.cell(0, 10, data['name'].upper(), ln=True, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.set_y(50)

    # --- TEMPLATE 2: CLASSIC BLACK ---
    elif style == "Classic Black":
        pdf.set_font("Arial", 'B', 22)
        pdf.cell(0, 15, data['name'], ln=True, align='L')
        pdf.line(10, 25, 200, 25)
        pdf.set_y(30)

    # --- TEMPLATE 3: CREATIVE SIDEBAR ---
    elif style == "Creative Sidebar":
        pdf.set_fill_color(40, 40, 40)
        pdf.rect(0, 0, 65, 297, 'F') # Left Sidebar
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 16)
        pdf.set_xy(5, 20)
        pdf.multi_cell(55, 10, data['name'].upper(), align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(70, 20)

    # --- TEMPLATE 4: ELEGANT GOLD ---
    elif style == "Elegant Gold":
        pdf.set_draw_color(212, 175, 55) # Gold
        pdf.set_line_width(1)
        pdf.rect(5, 5, 200, 287) # Border
        pdf.set_font("Times", 'B', 24)
        pdf.set_text_color(150, 120, 20)
        pdf.cell(0, 20, data['name'], ln=True, align='C')
        pdf.set_text_color(0, 0, 0)

    # --- TEMPLATE 5: MINIMALIST ---
    else:
        pdf.set_font("Courier", 'B', 20)
        pdf.cell(0, 10, data['name'], ln=True, align='C')
        pdf.ln(10)

    # --- COMMON CONTENT LOGIC ---
    # (Yeh sabhi templates mein information bharta hai)
    sections = [
        ("Summary", data.get('summary')),
        ("Experience", data.get('experience')),
        ("Education", data.get('education')),
        ("Skills", data.get('skills'))
    ]
    
    for title, content in sections:
        if has_content(content):
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, title.upper(), ln=True)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 6, content)
            pdf.ln(5)
            
    return pdf.output(dest='S').encode('latin-1')

# ===== Step 3: Input Steps =====
if st.session_state.step == 1:
    st.title("👤 Personal Details")
    st.session_state.user_data['name'] = st.text_input("Full Name", value=st.session_state.user_data.get('name', ''))
    st.session_state.user_data['email'] = st.text_input("Email")
    if st.button("Next"): st.session_state.step = 2; st.rerun()

elif st.session_state.step == 2:
    st.title("📄 Experience & Skills")
    st.session_state.user_data['experience'] = st.text_area("Experience")
    st.session_state.user_data['skills'] = st.text_area("Skills")
    st.session_state.user_data['education'] = st.text_area("Education")
    st.session_state.user_data['summary'] = st.text_area("Summary")
    if st.button("See Templates 🎨"): st.session_state.step = 3; st.rerun()

# ===== Step 4: 5 Template Gallery =====
elif st.session_state.step == 3:
    st.title("🎨 Select Your Favorite Template")
    
    col1, col2, col3 = st.columns(3)
    
    t_list = [
        ("Modern Blue", "Professional with Blue Header"),
        ("Classic Black", "Clean & Standard Layout"),
        ("Creative Sidebar", "Stylish Dark Sidebar"),
        ("Elegant Gold", "Premium Gold Border"),
        ("Minimalist", "Simple Courier Font Style")
    ]
    
    for i, (t_name, t_desc) in enumerate(t_list):
        # 3 columns mein distribute karna
        target_col = [col1, col2, col3][i % 3]
        with target_col:
            st.markdown(f'<div class="template-card">', unsafe_allow_html=True)
            # Yahan placeholder image hai, aap apni images dal sakte hain
            st.image(f"https://via.placeholder.com/200x250.png?text={t_name.replace(' ', '+')}")
            st.write(f"**{t_name}**")
            st.caption(t_desc)
            if st.button(f"Use {t_name}"):
                st.session_state.selected_style = t_name
                st.session_state.step = 4
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

# ===== Step 5: Final Download & Change Template =====
elif st.session_state.step == 4:
    st.success(f"Selected Design: {st.session_state.selected_style}")
    pdf_bytes = create_pdf(st.session_state.user_data, st.session_state.selected_style)
    
    st.download_button("📥 Download PDF", data=pdf_bytes, file_name="My_Resume.pdf", use_container_width=True)
    
    if st.button("🔄 Change Template (Go Back to Gallery)"):
        st.session_state.step = 3
        st.rerun()
