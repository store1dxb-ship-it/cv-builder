import streamlit as st
import requests
from weasyprint import HTML
from jinja2 import Template
import templates  # Importing the file created previously

# ==========================================
# 1. AI CONFIGURATION
# ==========================================
def get_ai_suggestions(role, info_type):
    # Note: Real environment mein API Key ko st.secrets mein rakhna behtar hota hai
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
        if st.button("Next: Choose Design 🎨"):
            st.session_state.user_data.update({
                "summary": summary, 
                "education": education, 
                "experience": experience
            })
            st.session_state.step = 3
            st.rerun()

# --- STEP 3: TEMPLATE SELECTION ---
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
            .thumb-box {
                width: 100%; height: 160px; border: 1px solid #ccc;
                border-radius: 5px; margin-bottom: 12px; background: white;
                overflow: hidden; position: relative; font-family: sans-serif;
                cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transition: transform 0.2s;
            }
            .thumb-box:hover { transform: scale(1.02); border-color: #007bff; }
            .t-name { font-weight: bold; font-size: 9px; margin-bottom: 2px; }
            .t-role { font-size: 7px; color: #555; margin-bottom: 5px; }
            .t-text { font-size: 5px; color: #666; line-height: 1.3; margin-bottom: 4px; text-align: justify; }
            .t-head { font-weight: bold; font-size: 6px; margin-top: 6px; margin-bottom: 3px; text-transform: uppercase; }
            .t-pill { display: inline-block; background: #eee; padding: 1px 3px; border-radius: 2px; font-size: 4px; margin-right: 2px;}

            /* Specific Styles */
            .tb-header { border-bottom: 3px solid #2c3e50; padding: 6px; margin-bottom: 5px; background: #f8f9fa; }
            .tm-box { padding: 10px; text-align: center; } .tm-line { border-bottom: 1px solid #333; margin: 6px 30%; }
            .tg-container { display: flex; height: 100%; } .tg-left { width: 32%; background: #27ae60; padding: 6px; color: white; } .tg-right { width: 68%; padding: 6px; }
            .tr-header { background: #c0392b; color: white; padding: 10px; }
            .tp-container { display: flex; height: 100%; } .tp-left { width: 65%; padding: 8px; } .tp-right { width: 35%; background: #f4ecf7; border-left: 3px solid #8e44ad; padding: 8px; }
        </style>
        """, unsafe_allow_html=True)

        # 1. Classic Blue
        st.markdown('<div class="thumb-box"><div class="tb-header"><div class="t-name" style="color:#2c3e50">VIKRAM MALHOTRA</div><div class="t-role">Senior Software Engineer</div></div><div style="padding:0 8px"><div class="t-head" style="color:#2c3e50">SUMMARY</div><div class="t-text">Results-oriented professional...</div><div class="t-head" style="color:#2c3e50">EXPERIENCE</div><div class="t-text"><b>Infosys</b> - Team Lead<br>Optimized database queries.</div></div></div>', unsafe_allow_html=True)
        if st.button("Select Classic Blue", key="btn1", use_container_width=True):
            st.session_state.selected_template = "Classic Blue"
        st.write("---")

        # 2. Modern Minimal
        st.markdown('<div class="thumb-box tm-box"><div class="t-name" style="font-family:serif; font-size:11px;">ADITI SHARMA</div><div class="t-role">Digital Marketing</div><div class="tm-line"></div><div style="text-align:left; margin-top:8px;"><div class="t-head">PROFILE</div><div class="t-text">Creative marketer...</div></div></div>', unsafe_allow_html=True)
        if st.button("Select Modern Minimal", key="btn2", use_container_width=True):
            st.session_state.selected_template = "Modern Minimal"
        st.write("---")

        # 3. Green Sidebar
        st.markdown('<div class="thumb-box"><div class="tg-container"><div class="tg-left"><div style="font-size:5px; color:white">Contact<br>Skills</div></div><div class="tg-right"><div class="t-name" style="color:#27ae60">RAHUL VERMA</div><div class="t-head">SUMMARY</div><div class="t-text">Data Scientist...</div></div></div></div>', unsafe_allow_html=True)
        if st.button("Select Green Sidebar", key="btn3", use_container_width=True):
            st.session_state.selected_template = "Green Sidebar"
        st.write("---")

        # 4. Bold Red
        st.markdown('<div class="thumb-box"><div class="tr-header"><div class="t-name" style="color:white">ANJALI KAPOOR</div></div><div style="padding:8px"><div class="t-head" style="color:#c0392b">SUMMARY</div><div class="t-text">HR professional...</div></div></div>', unsafe_allow_html=True)
        if st.button("Select Bold Red", key="btn4", use_container_width=True):
            st.session_state.selected_template = "Bold Red"
        st.write("---")

        # 5. Creative Purple
        st.markdown('<div class="thumb-box"><div class="tp-container"><div class="tp-left"><div class="t-name" style="color:#8e44ad">KARTIK REDDY</div><div class="t-head" style="background:#8e44ad; color:white;">EXPERIENCE</div></div><div class="tp-right"><div class="t-head">CONTACT</div></div></div></div>', unsafe_allow_html=True)
        if st.button("Select Creative Purple", key="btn5", use_container_width=True):
            st.session_state.selected_template = "Creative Purple"
            
        st.divider()
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
        
