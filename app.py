
import streamlit as st
import google.generativeai as genai
from xhtml2pdf import pisa
import io
import base64
from PIL import Image
import PyPDF2
import json

# ===== CONFIGURATION =====
# Aapki provide ki hui API Key yahan integrate kar di gayi hai
API_KEY = "AIzaSyBnzIDq_M918jBKRIerScQfOefHDO9J-VM" 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Helper Functions ---
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def get_image_base64(image_file):
    if image_file:
        img = Image.open(image_file)
        img.thumbnail((200, 200))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return base64.b64encode(buf.getvalue()).decode()
    return None

# --- AI Logic: Parse CV ---
def ai_parse_cv(text):
    prompt = f"""
    Extract information from the following text and return it ONLY as a JSON object.
    Keys: "name", "email", "location", "summary", "experience", "skills", "education".
    Text: {text}
    """
    try:
        response = model.generate_content(prompt)
        # Clean the response to get valid JSON
        clean_json = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(clean_json)
    except Exception as e:
        return None

# --- AI Logic: Keyword Suggestion ---
def ai_suggest_keywords(exp, jd):
    prompt = f"""
    Compare this Experience: {exp} 
    With this Job Description: {jd}. 
    Suggest 5-7 missing ATS-friendly keywords and skills as a bulleted list.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "AI is currently busy, please try again."

# --- HD HTML Template (Image Style) ---
def get_hd_template(data, img_b64):
    photo_html = f'<img src="data:image/png;base64,{img_b64}" style="width:100px; height:110px; border:2px solid #0056b3; float:right;">' if img_b64 else ""
    return f"""
    <html>
    <head>
        <style>
            @page {{ size: a4; margin: 0mm; }}
            body {{ font-family: Arial, sans-serif; color: #333; margin: 0; }}
            .sidebar {{ position: absolute; left: 0; top: 0; bottom: 0; width: 18px; background: #0056b3; }}
            .container {{ margin-left: 45px; padding: 40px; }}
            h1 {{ font-size: 26pt; margin: 0; text-transform: uppercase; color: #000; }}
            .contact-strip {{ background: #0056b3; color: white; padding: 8px 15px; font-size: 9pt; margin-top: 15px; }}
            h2 {{ font-size: 14pt; border-bottom: 2.5px solid #0056b3; padding-bottom: 4px; margin-top: 20px; text-transform: uppercase; color: #000; }}
            .box {{ font-size: 10pt; line-height: 1.5; margin-top: 5px; }}
        </style>
    </head>
    <body>
        <div class="sidebar"></div>
        <div class="container">
            <div style="float:left; width:70%;">
                <h1>{data.get('name', 'User Name')}</h1>
                <p style="color:#666; font-size:12pt; margin:5px 0;">Professional Resume</p>
            </div>
            <div style="float:right; width:25%; text-align:right;">{photo_html}</div>
            <div style="clear:both;"></div>
            <div class="contact-strip">Email: {data.get('email','')} | Location: {data.get('location','')}</div>
            
            <h2>Profile</h2><div class="box">{data.get('summary','')}</div>
            <h2>Experience</h2><div class="box">{str(data.get('experience','')).replace('\\n', '<br>')}</div>
            <h2>Skills</h2><div class="box">{data.get('skills','')}</div>
            <h2>Education</h2><div class="box">{str(data.get('education','')).replace('\\n', '<br>')}</div>
        </div>
    </body>
    </html>
    """

# ===== STREAMLIT UI =====
st.set_page_config(page_title="AI Resume Builder", layout="wide")
st.title("🤖 AI-Powered Professional CV Builder")

# Session State for persistence
if 'cv_data' not in st.session_state:
    st.session_state.cv_data = {"name":"", "email":"", "location":"", "summary":"", "experience":"", "skills":"", "education":""}

# Sidebar: Upload & Photo
st.sidebar.header("📁 Step 1: Upload & Photo")
old_cv = st.sidebar.file_uploader("Upload Old CV (PDF)", type=['pdf'])
if old_cv and st.sidebar.button("✨ Auto-Fill using AI"):
    with st.spinner("AI is analyzing your old CV..."):
        text_content = extract_text_from_pdf(old_cv)
        extracted_data = ai_parse_cv(text_content)
        if extracted_data:
            st.session_state.cv_data.update(extracted_data)
            st.sidebar.success("Data extracted successfully!")
        else:
            st.sidebar.error("Could not parse. Please fill manually.")

user_photo = st.sidebar.file_uploader("Upload Profile Photo", type=['jpg','png','jpeg'])

# Main Application
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🖋️ Edit Your Details")
    d = st.session_state.cv_data
    u_name = st.text_input("Full Name", d['name'])
    u_email = st.text_input("Email Address", d['email'])
    u_loc = st.text_input("Location", d['location'])
    u_sum = st.text_area("Summary / Profile", d['summary'], height=100)
    u_exp = st.text_area("Work Experience", d['experience'], height=200)
    u_skills = st.text_input("Skills (comma separated)", d['skills'])
    u_edu = st.text_area("Education Details", d['education'], height=100)
    
    current_data = {"name":u_name, "email":u_email, "location":u_loc, "summary":u_sum, "experience":u_exp, "skills":u_skills, "education":u_edu}

    st.divider()
    st.subheader("🎯 ATS Optimization")
    target_jd = st.text_area("Paste the Job Description you are targeting...")
    if st.button("🔍 Get AI Keyword Suggestions"):
        if target_jd:
            suggestions = ai_suggest_keywords(u_exp, target_jd)
            st.info(f"**Missing Keywords & Suggestions:**\n\n{suggestions}")
        else:
            st.warning("Please paste a Job Description first.")

with col2:
    st.subheader("👁️ Live CV Preview")
    img_b64 = get_image_base64(user_photo)
    html_cv = get_hd_template(current_data, img_b64)
    
    # Displaying the resume in a preview box
    st.components.v1.html(html_cv, height=800, scrolling=True)

    if st.button("📥 Generate & Download PDF"):
        buf = io.BytesIO()
        pisa.CreatePDF(html_cv, dest=buf)
        st.download_button(
            label="Download PDF Resume",
            data=buf.getvalue(),
            file_name=f"{u_name}_Professional_CV.pdf",
            mime="application/pdf"
        )
