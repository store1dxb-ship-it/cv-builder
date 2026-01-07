import streamlit as st
import requests
from weasyprint import HTML
from jinja2 import Template
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
    
    col_ai_1, col_ai_2 = st.columns(2)
    with col_ai_1:
        if st.button("✨ Auto-Write Summary"):
            with st.spinner("AI is writing summary..."):
                suggestion = get_ai_suggestions(role, "summary")
                st.session_state.user_data['summary'] = suggestion
                st.rerun()

    summary = st.text_area("Professional Summary", value=st.session_state.user_data.get('summary', ''), height=150)
    experience = st.text_area("Experience Details", value=st.session_state.user_data.get('experience', ''), placeholder="Enter your work history...", height=150)
    education = st.text_area("Education Details", value=st.session_state.user_data.get('education', ''), placeholder="Enter your degrees...", height=100)

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

# --- STEP 3: TEMPLATE SELECTION (BUTTON VERSION) ---
elif st.session_state.step == 3:
    st.header("🏆 Step 3: Choose Your Professional Template")
    
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("🎨 Select Design")
        
        # --- CSS Styles ---
        st.markdown("""
        <style>
            .thumb-box {
                width: 100%; min-height: 150px; border: 1px solid #ccc;
                border-radius: 5px; margin-bottom: 5px; background: white;
                padding: 0; overflow: hidden;
            }
            .t-name { font-weight: bold; font-size: 10px; color: black; margin: 5px; }
            .t-text { font-size: 6px; color: #555; margin: 5px; line-height: 1.2; }
            /* Specifics */
            .tb-head { background: #f8f9fa; border-bottom: 3px solid #2c3e50; padding: 5px; }
            .tg-left { background: #27ae60; width: 30%; height: 150px; float: left; }
            .tr-head { background: #c0392b; color: white; padding: 10px; }
            .tp-right { border-left: 3px solid #8e44ad; background: #f4ecf7; height: 150px; width: 35%; float: right; }
        </style>
        """, unsafe_allow_html=True)

        # 1. Classic Blue
        st.markdown('<div class="thumb-box"><div class="tb-head"><div class="t-name" style="color:#2c3e50">VIKRAM MALHOTRA</div></div><div class="t-text">Senior Engineer<br><br><b>SUMMARY</b><br>Experienced professional...</div></div>', unsafe_allow_html=True)
        if st.button("Select Classic Blue", use_container_width=True):
            st.session_state.selected_template = "Classic Blue"
        st.write("---")

        # 2. Modern Minimal
        st.markdown('<div class="thumb-box" style="text-align:center; padding-top:10px;"><div class="t-name" style="font-family:serif">ADITI SHARMA</div><hr style="margin:5px 30%"><div class="t-text" style="text-align:left; padding-left:10px">Digital Marketing<br><br><b>PROFILE</b><br>Creative marketer...</div></div>', unsafe_allow_html=True)
        if st.button("Select Modern Minimal", use_container_width=True):
            st.session_state.selected_template = "Modern Minimal"
        st.write("---")

        # 3. Green Sidebar
        st.markdown('<div class="thumb-box"><div class="tg-left"></div><div style="margin-left:32%; padding:5px;"><div class="t-name" style="color:#27ae60">RAHUL VERMA</div><div class="t-text">Data Scientist...</div></div></div>', unsafe_allow_html=True)
        if st.button("Select Green Sidebar", use_container_width=True):
            st.session_state.selected_template = "Green Sidebar"
        st.write("---")

        # 4. Bold Red
        st.markdown('<div class="thumb-box"><div class="tr-head"><div class="t-name" style="color:white">ANJALI KAPOOR</div></div><div class="t-text">HR Professional...</div></div>', unsafe_allow_html=True)
        if st.button("Select Bold Red", use_container_width=True):
            st.session_state.selected_template = "Bold Red"
        st.write("---")

        # 5. Creative Purple
        st.markdown('<div class="thumb-box"><div class="tp-right"></div><div style="padding:10px;"><div class="t-name" style="color:#8e44ad">KARTIK REDDY</div><div class="t-text">UX Designer...</div></div></div>', unsafe_allow_html=True)
        if st.button("Select Creative Purple", use_container_width=True):
            st.session_state.selected_template = "Creative Purple"
            
        st.divider()
        if st.button("⬅️ Edit Data", key="back_btn"):
            st.session_state.step = 2
            st.rerun()

    with col_right:
        st.success(f"✅ Selected Style: **{st.session_state.selected_template}**")
        st.subheader("Live Preview (Full Size)")
        
        # --- GENERATE PREVIEW ---
        html_template_string = templates.all_templates[st.session_state.selected_template]
        jinja_template = Template(html_template_string)
        filled_html = jinja_template.render(**st.session_state.
                                            
