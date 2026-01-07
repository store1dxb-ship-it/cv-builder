import streamlit as st
import requests
from weasyprint import HTML
from jinja2 import Template
from st_click_detector import click_detector
import templates  # Importing your templates.py file

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
# Initialize selected template if not present
if 'selected_template' not in st.session_state: st.session_state.selected_template = "Classic Blue"

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

# --- STEP 3: TEMPLATE SELECTION (CLICKABLE THUMBNAILS) ---
elif st.session_state.step == 3:
    st.header("🏆 Step 3: Choose Your Professional Template")
    
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("🎨 Select Design")
        st.caption("Click on a template to select it.")
        
        # --- CSS STYLES ---
        css_content = """
            .thumb-box {
                width: 100%; min-height: 150px; border: 1px solid #ddd;
                border-radius: 8px; margin-bottom: 15px; background: white;
                overflow: hidden; cursor: pointer; position: relative;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: all 0.2s;
            }
            .thumb-box:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            
            /* Selected State Highlight */
            .selected-img { border: 3px solid #007bff; transform: scale(1.02); }
            
            /* Text Styles */
            .t-name { font-weight: bold; font-size: 10px; margin-bottom: 3px; color: black; }
            .t-role { font-size: 8px; color: #555; margin-bottom: 5px; }
            .t-text { font-size: 6px; color: #666; line-height: 1.3; margin-bottom: 4px; }
            .t-head { font-weight: bold; font-size: 7px; margin-top: 6px; margin-bottom: 3px; text-transform: uppercase; color: black; }
            
            /* Specific Styles */
            .tb-header { border-bottom: 3px solid #2c3e50; padding: 8px; background: #f8f9fa; }
            .tm-box { padding: 12px; text-align: center; } .tm-line { border-bottom: 1px solid #333; margin: 6px 30%; }
            .tg-container { display: flex; height: 100%; min-height: 150px; } .tg-left { width: 32%; background: #27ae60; padding: 8px; color: white; } .tg-right { width: 68%; padding: 8px; }
            .tr-header { background: #c0392b; color: white; padding: 12px; }
            .tp-container { display: flex; height: 100%; min-height: 150px; } .tp-left { width: 65%; padding: 10px; } .tp-right { width: 35%; background: #f4ecf7; border-left: 3px solid #8e44ad; padding: 10px; }
        """

        # --- HTML BUILDER FOR THUMBNAILS ---
        sel = st.session_state.selected_template
        
        def get_class(name):
            return "thumb-box selected-img" if sel == name else "thumb-box"

        html_code = f"""
        <div id='Classic Blue' class='{get_class("Classic Blue")}'>
            <div class='tb-header'><div class='t-name' style='color:#2c3e50'>VIKRAM MALHOTRA</div><div class='t-role'>Senior Engineer</div></div>
            <div style='padding:8px'><div class='t-head' style='color:#2c3e50'>SUMMARY</div><div class='t-text'>Results-oriented professional...</div></div>
        </div>

        <div id='Modern Minimal' class='{get_class("Modern Minimal")}'>
            <div class='tm-box'>
                <div class='t-name' style='font-family:serif; font-size:12px;'>ADITI SHARMA</div><div class='t-role'>Digital Marketing</div>
                <div class='tm-line'></div><div style='text-align:left; margin-top:8px;'><div class='t-head'>PROFILE</div><div class='t-text'>Creative marketer...</div></div>
            </div>
        </div>

        <div id='Green Sidebar' class='{get_class("Green Sidebar")}'>
            <div class='tg-container'>
                <div class='tg-left'><div style='font-size:6px; color:white'>Contact<br>Skills</div></div>
                <div class='tg-right'><div class='t-name' style='color:#27ae60'>RAHUL VERMA</div><div class='t-head'>SUMMARY</div><div class='t-text'>Data Scientist...</div></div>
            </div>
        </div>

        <div id='Bold Red' class='{get_class("Bold Red")}'>
            <div class='tr-header'><div class='t-name' style='color:white'>ANJALI KAPOOR</div></div>
            <div style='padding:10px'><div class='t-head' style='color:#c0392b'>SUMMARY</div><div class='t-text'>HR professional...</div></div>
        </div>

        <div id='Creative Purple' class='{get_class("Creative Purple")}'>
            <div class='tp-container'>
                <div class='tp-left'><div class='t-name' style='color:#8e44ad'>KARTIK REDDY</div><div class='t-head' style='background:#8e44ad; color:white;'>EXPERIENCE</div></div>
                <div class='tp-right'><div class='t-head'>CONTACT</div></div>
            </div>
        </div>
        """

        # --- CLICK DETECTOR ---
        clicked_id = click_detector(html_code, css_content)

        if clicked_id and clicked_id != st.session_state.selected_template:
            st.session_state.selected_template = clicked_id
            st.rerun()
            
        st.divider()
        if st.button("⬅️ Edit Data", key="back_btn"):
            st.session_state.step = 2
            st.rerun()

    with col_right:
        st.success(f"✅ Selected Style: **{st.session_state.selected_template}**")
        st.subheader("Live Preview (Full Size)")
        
        # --- GENERATE & PREVIEW ---
        html_template_string = templates.all_templates[st.session_state.selected_template]
        jinja_template = Template(html_template_string)
        filled_html = jinja_template.render(**st.session_state.user_data)
        
        # PREVIEW FIX: FORCE WHITE BACKGROUND
        preview_html = f"""
        <style>
            body {{ background-color: white !important; color: black !important; }}
        </style>
        {filled_html}
        """
        
        # SHOW HTML PREVIEW
        st.components.v1.html(preview_html, height=800, scrolling=True)
        
        # --- DOWNLOAD BUTTON ---
        # Generate PDF Bytes
        pdf_bytes = HTML(string=filled_html).write_pdf()
        
        st.download_button(
            label=f"⬇️ Download {st.session_state.selected_template} PDF",
            data=pdf_bytes,
            file_name=f"{st.session_state.user_data.get('name', 'Resume')}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
