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
      # --- STEP 3: TEMPLATE SELECTION (REALISTIC & FULL) ---
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
                height: 160px; /* Height badhai taaki full dikhe */
                border: 1px solid #ccc;
                border-radius: 5px;
                margin-bottom: 12px;
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
            .t-name { font-weight: bold; font-size: 9px; margin-bottom: 2px; }
            .t-role { font-size: 7px; color: #555; margin-bottom: 5px; }
            .t-text { font-size: 5px; color: #666; line-height: 1.3; margin-bottom: 4px; text-align: justify; }
            .t-head { font-weight: bold; font-size: 6px; margin-top: 6px; margin-bottom: 3px; text-transform: uppercase; }
            .t-pill { display: inline-block; background: #eee; padding: 1px 3px; border-radius: 2px; font-size: 4px; margin-right: 2px;}

            /* 1. Classic Blue Specifics */
            .tb-header { border-bottom: 3px solid #2c3e50; padding: 6px; margin-bottom: 5px; background: #f8f9fa; }
            .tb-name { color: #2c3e50; }
            .tb-body { padding: 0 8px; }

            /* 2. Modern Minimal Specifics */
            .tm-box { padding: 10px; text-align: center; }
            .tm-name { font-family: serif; font-size: 11px; }
            .tm-line { border-bottom: 1px solid #333; margin: 6px 30%; }
            .tm-body { text-align: left; margin-top: 8px; padding: 0 5px; }

            /* 3. Green Sidebar Specifics */
            .tg-container { display: flex; height: 100%; }
            .tg-left { width: 32%; background: #27ae60; padding: 6px; color: white; }
            .tg-right { width: 68%; padding: 6px; }
            .tg-white-text { color: white; font-size: 5px; opacity: 0.9; margin-bottom: 4px;}
            
            /* 4. Bold Red Specifics */
            .tr-header { background: #c0392b; color: white; padding: 10px; }
            .tr-body { padding: 8px; }
            
            /* 5. Creative Purple Specifics */
            .tp-container { display: flex; height: 100%; }
            .tp-left { width: 65%; padding: 8px; }
            .tp-right { width: 35%; background: #f4ecf7; border-left: 3px solid #8e44ad; padding: 8px; }
            .tp-name { color: #8e44ad; }
        </style>
        """, unsafe_allow_html=True)

        # --- THUMBNAIL 1: CLASSIC BLUE ---
        st.markdown("""
        <div class="thumb-box">
            <div class="tb-header">
                <div class="t-name tb-name">VIKRAM MALHOTRA</div>
                <div class="t-role">Senior Software Engineer</div>
            </div>
            <div class="tb-body">
                <div class="t-head" style="color:#2c3e50">PROFESSIONAL SUMMARY</div>
                <div class="t-text">Results-oriented professional with 8+ years of experience in software development and team leadership. Proven track record of delivering scalable solutions.</div>
                <div class="t-head" style="color:#2c3e50">EXPERIENCE</div>
                <div class="t-text"><b>Infosys Ltd, Bangalore</b> - Team Lead (2018-Present)<br>• Led a team of 15 developers for a fintech project.<br>• Optimized database queries reducing load time by 40%.</div>
                <div class="t-text"><b>TCS, Mumbai</b> - Developer (2015-2018)<br>• Developed REST APIs for banking modules.<br>• Collaborated with cross-functional teams.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Classic Blue", key="btn1", use_container_width=True):
            st.session_state.selected_template = "Classic Blue"
        st.write("---")

        # --- THUMBNAIL 2: MODERN MINIMAL ---
        st.markdown("""
        <div class="thumb-box tm-box">
            <div class="t-name tm-name">ADITI SHARMA</div>
            <div class="t-role">Digital Marketing Specialist</div>
            <div class="tm-line"></div>
            <div class="tm-body">
                <div class="t-head">PROFILE</div>
                <div class="t-text">Creative marketer with expertise in SEO, SEM, and Social Media strategies. Skilled in driving brand awareness and high ROI campaigns.</div>
                <div class="t-head">WORK HISTORY</div>
                <div class="t-text"><b>Zomato</b> (2020-Present) - Marketing Manager<br>Increased organic traffic by 150% in 2 years.</div>
                <div class="t-text"><b>Swiggy</b> (2018-2020) - SEO Analyst<br>Managed monthly ad budget of ₹5 Lakhs.</div>
                <div class="t-head">SKILLS</div>
                <div class="t-text">Google Analytics, SEO, Content Strategy, PPC</div>
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
                    <div style="font-weight:bold; font-size:6px; margin-bottom:5px;">CONTACT</div>
                    <div class="tg-white-text">+91 98765 43210<br>rahul.verma@email.com<br>Pune, Maharashtra</div>
                    <div style="font-weight:bold; font-size:6px; margin-top:10px;">SKILLS</div>
                    <div class="tg-white-text">• Python Programming<br>• Data Analysis<br>• Machine Learning<br>• SQL & NoSQL</div>
                    <div style="font-weight:bold; font-size:6px; margin-top:10px;">LANGUAGES</div>
                    <div class="tg-white-text">English, Hindi, Marathi</div>
                </div>
                <div class="tg-right">
                    <div class="t-name" style="color:#27ae60; font-size:11px;">RAHUL VERMA</div>
                    <div class="t-role">Data Scientist</div>
                    <div class="t-head">SUMMARY</div>
                    <div class="t-text">Data Scientist with 5 years of experience in predictive modeling and data mining. Passionate about solving complex business problems using AI.</div>
                    <div class="t-head">EXPERIENCE</div>
                    <div class="t-text"><b>Wipro Technologies</b><br>Senior Analyst | 2019 - Present<br>• Built recommendation engines for retail clients.<br>• Automated reporting dashboards using PowerBI.</div>
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
                <div class="t-name" style="color:white; font-size:12px;">ANJALI KAPOOR</div>
                <div class="t-role" style="color:white; opacity:0.9;">HR Manager</div>
            </div>
            <div class="tr-body">
                <div class="t-head" style="color:#c0392b">PROFESSIONAL SUMMARY</div>
                <div class="t-text">Dedicated HR professional with strong background in talent acquisition, employee relations, and policy formulation.</div>
                <div class="t-head" style="color:#c0392b">EXPERIENCE</div>
                <div class="t-text"><b>HCL Technologies</b> - HR Business Partner<br>2017 - Present | Noida, India<br>• Managed recruitment for 500+ technical roles.<br>• Implemented new employee engagement programs.</div>
                <div class="t-head" style="color:#c0392b">CORE COMPETENCIES</div>
                <span class="t-pill">Recruitment</span> <span class="t-pill">Payroll</span> <span class="t-pill">Conflict Resolution</span>
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
                    <div class="t-name tp-name">KARTIK REDDY</div>
                    <div class="t-role">UX/UI Designer</div>
                    <div class="t-head" style="background:#8e44ad; color:white; padding:1px 3px; display:inline-block;">EXPERIENCE</div>
                    <div class="t-text" style="margin-top:2px;"><b>Flipkart</b> - Product Designer<br>2020 - Present<br>• Redesigned the checkout flow increasing conversion by 12%.<br>• Created design systems for mobile app.</div>
                    <div class="t-text"><b>Myntra</b> - UI Designer<br>2018 - 2020<br>• Designed marketing banners and landing pages.</div>
                </div>
                <div class="tp-right">
                    <div class="t-head">CONTACT</div>
                    <div class="t-text">kartik.r@email.com<br>+91 99887 76655<br>Hyderabad</div>
                    <div class="t-head">EDUCATION</div>
                    <div class="t-text"><b>B.Des in Interaction Design</b><br>NID, Ahmedabad (2018)</div>
                    <div class="t-head">TOOLS</div>
                    <div class="t-text">Figma, Adobe XD, Sketch</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
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
# --- FILE ENDS HERE (Make sure to delete any duplicate code below this line) ---

        
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
        
