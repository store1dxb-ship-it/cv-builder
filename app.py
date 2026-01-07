import streamlit as st
import requests
from weasyprint import HTML
from jinja2 import Template
import templates  # Importing the file we created above

# ==========================================
# 1. AI CONFIGURATION
# ==========================================
def get_ai_suggestions(role, info_type):
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg"
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
# 2. STREAMLIT UI SETUP
# ==========================================
st.set_page_config(page_title="AI Resume Pro", page_icon="📝", layout="wide")

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
        
        if st.form_submit_button("Next: AI Content ➡️"):
            if name and role:
                st.session_state.user_data.update({"name": name, "email": email, "phone": phone, "role": role})
                st.session_state.step = 2
                st.rerun()
            else:
                st.error("Please fill Name and Role!")

# --- STEP 2: AI Content Generation ---
elif st.session_state.step == 2:
    st.header("🤖 Step 2: Content Generation")
    role = st.session_state.user_data['role']
    
    # AI Buttons
    col_ai_1, col_ai_2 = st.columns(2)
    with col_ai_1:
        if st.button("✨ Auto-Write Summary"):
            with st.spinner("AI is writing summary..."):
                suggestion = get_ai_suggestions(role, "summary")
                st.session_state.user_data['summary'] = suggestion
                st.rerun()

    # Input Fields
    summary = st.text_area("Professional Summary", value=st.session_state.user_data.get('summary', ''), height=150)
    experience = st.text_area("Experience Details", value=st.session_state.user_data.get('experience', ''), placeholder="Enter your work history here...", height=150)
    education = st.text_area("Education Details", value=st.session_state.user_data.get('education', ''), placeholder="Enter your degrees here...", height=100)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⬅️ Back"):
            st.session_state.step = 1
            st.rerun()
    with col3:
        # Saving data and moving to new template design step
        if st.button("Next: Choose Design 🎨"):
            st.session_state.user_data.update({
                "summary": summary, 
                "education": education, 
                "experience": experience
            })
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: TEMPLATE SELECTION (REALISTIC PREVIEW) ---
elif st.session_state.step == 3:
    st.header("🏆 Step 3: Choose Your Professional Template")
    
    # Initialize selection
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = "Classic Blue"

    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("🎨 Select Design")
        
        # --- CSS FOR REALISTIC MINI THUMBNAILS ---
        st.markdown("""
        <style>
            /* Base Box Style */
            .thumb-box {
                width: 100%;
                height: 140px;
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-bottom: 10px;
                background: white;
                overflow: hidden;
                position: relative;
                font-family: sans-serif;
                cursor: pointer;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            .thumb-box:hover { transform: scale(1.02); border-color: #007bff; }
            
            /* Common Text Styles */
            .t-name { font-weight: bold; font-size: 8px; margin-bottom: 2px; }
            .t-role { font-size: 6px; color: #555; margin-bottom: 4px; }
            .t-text { font-size: 4px; color: #777; line-height: 1.2; margin-bottom: 3px; text-align: justify; }
            .t-head { font-weight: bold; font-size: 5px; margin-top: 5px; margin-bottom: 2px; text-transform: uppercase; }
            
            /* 1. Classic Blue Specifics */
            .tb-header { border-bottom: 2px solid #2c3e50; padding: 5px; margin-bottom: 5px; }
            .tb-name { color: #2c3e50; }
            .tb-body { padding: 0 5px; }

            /* 2. Modern Minimal Specifics */
            .tm-box { padding: 10px; text-align: center; }
            .tm-name { font-family: serif; font-size: 10px; }
            .tm-line { border-bottom: 1px solid #000; margin: 5px 30%; }
            .tm-body { text-align: left; margin-top: 5px; }

            /* 3. Green Sidebar Specifics */
            .tg-container { display: flex; height: 100%; }
            .tg-left { width: 30%; background: #27ae60; padding: 5px; color: white; }
            .tg-right { width: 70%; padding: 5px; }
            .tg-white-text { color: white; font-size: 4px; }
            
            /* 4. Bold Red Specifics */
            .tr-header { background: #c0392b; color: white; padding: 8px; }
            .tr-body { padding: 5px; }
            .tr-pill { display: inline-block; background: #eee; padding: 1px 3px; border-radius: 2px; font-size: 3px; }

            /* 5. Creative Purple Specifics */
            .tp-container { display: flex; height: 100%; }
            .tp-left { width: 65%; padding: 5px; }
            .tp-right { width: 35%; background: #f4ecf7; border-left: 3px solid #8e44ad; padding: 5px; }
            .tp-name { color: #8e44ad; }
        </style>
        """, unsafe_allow_html=True)

        # --- THUMBNAIL 1: CLASSIC BLUE ---
        st.markdown("""
        <div class="thumb-box">
            <div class="tb-header">
                <div class="t-name tb-name">JOHN DOE</div>
                <div class="t-role">Project Manager</div>
            </div>
            <div class="tb-body">
                <div class="t-head" style="color:#2c3e50">SUMMARY</div>
                <div class="t-text">Experienced manager with 10+ years in IT sector...</div>
                <div class="t-head" style="color:#2c3e50">EXPERIENCE</div>
                <div class="t-text"><b>Infosys</b> - Senior Manager<br>Led team of 20 people...</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Classic Blue", key="btn1", use_container_width=True):
            st.session_state.selected_template = "Classic Blue"

        st.write("---")

        # --- THUMBNAIL 2: MODERN MINIMAL ---
        st.markdown("""
        <div class="thumb-box tm-box">
            <div class="t-name tm-name">JOHN DOE</div>
            <div class="t-role">Project Manager</div>
            <div class="tm-line"></div>
            <div class="tm-body">
                <div class="t-head">PROFILE</div>
                <div class="t-text">Detailed oriented professional...</div>
                <div class="t-head">WORK HISTORY</div>
                <div class="t-text"><b>TCS</b> (2020-Present)<br>Managed cloud migration projects.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Modern Minimal", key="btn2", use_container_width=True):
            st.session_state.selected_template = "Modern Minimal"

        st.write("---")

        # --- THUMBNAIL 3: GREEN SIDEBAR ---
        st.markdown("""
        <div class="thumb-box">
            <div class="tg-container">
                <div class="tg-left">
                    <div style="font-weight:bold; font-size:5px; margin-bottom:5px;">CONTACT</div>
                    <div class="tg-white-text">Phone<br>Email<br>City</div>
                    <div style="font-weight:bold; font-size:5px; margin-top:10px;">SKILLS</div>
                    <div class="tg-white-text">- Python<br>- Agile</div>
                </div>
                <div class="tg-right">
                    <div class="t-name" style="color:#27ae60; font-size:10px;">JOHN DOE</div>
                    <div class="t-role">Manager</div>
                    <div class="t-head">SUMMARY</div>
                    <div class="t-text">Passionate leader...</div>
                    <div class="t-head">EXPERIENCE</div>
                    <div class="t-text"><b>Wipro</b><br>Delivered high value...</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Green Sidebar", key="btn3", use_container_width=True):
            st.session_state.selected_template = "Green Sidebar"

        st.write("---")

        # --- THUMBNAIL 4: BOLD RED ---
        st.markdown("""
        <div class="thumb-box">
            <div class="tr-header">
                <div class="t-name" style="color:white;">JOHN DOE</div>
                <div class="t-role" style="color:white; opacity:0.8;">Project Manager</div>
            </div>
            <div class="tr-body">
                <div class="t-head" style="color:#c0392b">SUMMARY</div>
                <div class="t-text">Strategic planner...</div>
                <div class="t-head" style="color:#c0392b">EXPERIENCE</div>
                <div class="t-text"><b>HCL Tech</b><br>Team Lead for 5 years.</div>
                <div class="t-head" style="color:#c0392b">SKILLS</div>
                <span class="tr-pill">JIRA</span> <span class="tr-pill">Scrum</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Bold Red", key="btn4", use_container_width=True):
            st.session_state.selected_template = "Bold Red"

        st.write("---")

        # --- THUMBNAIL 5: CREATIVE PURPLE ---
        st.markdown("""
        <div class="thumb-box">
            <div class="tp-container">
                <div class="tp-left">
                    <div class="t-name tp-name">JOHN DOE</div>
                    <div class="t-role">Manager</div>
                    <div class="t-head" style="background:#8e44ad; color:white; padding:1px 3px; display:inline-block;">EXPERIENCE</div>
                    <div class="t-text" style="margin-top:2px;"><b>IBM</b><br>Senior Analyst.</div>
                </div>
                <div class="tp-right">
                    <div class="t-head">CONTACT</div>
                    <div class="t-text">Email<br>Phone</div>
                    <div class="t-head">EDUCATION</div>
                    <div class="t-text">MBA - 2015</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Creative Purple", key="btn5", use_container_width=True):
            st.session_state.selected_template = "Creative Purple"
            
        if st.button("⬅️ Edit Data", key="back_btn"):
            st.session_state.step = 2
            st.rerun()

    with col_right:
        st.success(f"✅ Currently Viewing: **{st.session_state.selected_template}**")
        st.subheader("Live Preview (Full Size)")
        
        # Render HTML with User Data
        html_template_string = templates.all_templates[st.session_state.selected_template]
        jinja_template = Template(html_template_string)
        filled_html = jinja_template.render(**st.session_state.user_data)
        
        # Show HTML Preview
        st.components.v1.html(filled_html, height=800, scrolling=True)
        
        # Generate PDF
        pdf_bytes = HTML(string=filled_html).write_pdf()
        
        st.download_button(
            label=f"⬇️ Download {st.session_state.selected_template} PDF",
            data=pdf_bytes,
            file_name=f"{st.session_state.user_data.get('name', 'Resume')}.pdf",
            mime="application/pdf",
            type="primary"
        )

        
        # Get Template String
        html_template_string = templates.all_templates[selected_template_name]
        
        # Render HTML with User Data
        jinja_template = Template(html_template_string)
        filled_html = jinja_template.render(**st.session_state.user_data)
        
        # Show HTML Preview
        st.components.v1.html(filled_html, height=600, scrolling=True)
        
        # Generate PDF with WeasyPrint
        pdf_bytes = HTML(string=filled_html).write_pdf()
        
        st.download_button(
            label=f"⬇️ Download {selected_template_name} PDF",
            data=pdf_bytes,
            file_name="My_Professional_Resume.pdf",
            mime="application/pdf",
            type="primary"
        )
        
