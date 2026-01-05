import streamlit as st
from fpdf import FPDF
import requests

# ==========================================
# 1. AI CONFIGURATION (Gemini – Stable)
# ==========================================
def get_ai_suggestions(role, info_type, skills=""):
    api_key = st.secrets.get("GEMINI_API_KEY", "")  # safer
    model = "gemini-1.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"

    prompts = {
        "skills": f"List 8 professional skills for a {role}. Comma separated.",
        "summary": f"Write a short professional summary for a {role} using skills: {skills}.",
        "experience": f"Write 3 resume bullet points for {role}.",
        "projects": f"List 2 important projects for a {role}.",
        "achievements": f"List 2 professional achievements for a {role}."
    }

    prompt = prompts.get(info_type, "")
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        res = requests.post(url, json=data, timeout=10)
        if res.status_code == 200:
            return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "AI service unavailable."

    return ""

# ==========================================
# 2. PDF GENERATION
# ==========================================
class PDF(FPDF):
    def header(self):
        if hasattr(self, "r"):
            self.set_fill_color(self.r, self.g, self.b)
            self.rect(0, 0, 210, 22, "F")

def create_pdf(data):
    pdf = PDF()
    pdf.r, pdf.g, pdf.b = data.get("color_rgb", (0, 0, 0))
    pdf.add_page()

    pdf.set_y(28)
    pdf.set_font("Arial", "B", 22)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, data["name"].upper(), ln=True)

    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(pdf.r, pdf.g, pdf.b)
    pdf.cell(0, 8, data["role"].upper(), ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(
        0,
        8,
        f"{data['email']} | {data['phone']} | {data['city']}, {data['country']}",
        ln=True,
    )
    pdf.ln(5)

    sections = [
        ("SUMMARY", "summary"),
        ("SKILLS", "skills"),
        ("EXPERIENCE", "experience"),
        ("PROJECTS", "projects"),
        ("EDUCATION", "education"),
        ("CERTIFICATIONS", "certs"),
        ("ACHIEVEMENTS", "achievements"),
    ]

    for title, key in sections:
        content = data.get(key, "")
        if content:
            pdf.set_font("Arial", "B", 12)
            pdf.set_text_color(pdf.r, pdf.g, pdf.b)
            pdf.cell(0, 8, title, ln=True)
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 5, content)
            pdf.ln(3)

    return pdf.output(dest="S").encode("latin-1", "ignore")

# ==========================================
# 3. STREAMLIT UI
# ==========================================
st.set_page_config("AI Resume Pro", layout="wide", page_icon="📄")

if "step" not in st.session_state:
    st.session_state.step = 0
if "user_data" not in st.session_state:
    st.session_state.user_data = {}

# ==========================================
# STEP 0 – TEMPLATE SELECTION
# ==========================================
if st.session_state.step == 0:
    st.title("🚀 Select Your Professional Template")

    templates = [
        {
            "name": "Pankaj Kumar",
            "role": "Senior Project Manager",
            "type": "Executive Class",
            "border": "border-left:8px solid",
            "colors": {"Navy": (0, 32, 96), "Teal": (0, 128, 128)},
            "summary": "Senior Project Manager with 10+ years of experience.",
            "skills": "Agile, Scrum, Budgeting",
            "experience": "• Senior PM – TechFlow\n• Project Lead – BuildCorp",
            "projects": "• AI Migration\n• Smart City Pilot",
        },
        {
            "name": "Punit Yadav",
            "role": "Lead Data Scientist",
            "type": "Modern Tech",
            "border": "border-top:8px solid",
            "colors": {"Crimson": (139, 0, 0), "Blue": (0, 0, 255)},
            "summary": "Data Scientist with ML & AI expertise.",
            "skills": "Python, ML, SQL",
            "experience": "• Lead DS – DataWiz\n• Analyst – FinTech",
            "projects": "• Churn Model\n• NLP Bot",
        },
        {
            "name": "Rashmi Desai",
            "role": "Senior UI/UX Designer",
            "type": "Creative Minimal",
            "border": "border:2px solid",
            "colors": {"Black": (0, 0, 0), "HotPink": (255, 20, 147)},
            "summary": "Creative UI/UX Designer with 7+ years experience.",
            "skills": "Figma, UX Research",
            "experience": "• Senior Designer – CreativeBox\n• UI Designer – Webify",
            "projects": "• App Redesign\n• Banking UI",
        },
    ]

    cols = st.columns(3)

    for i, temp in enumerate(templates):
        with cols[i]:
            color_name = st.radio(
                "Pick Color",
                list(temp["colors"].keys()),
                key=f"color_{i}",
                horizontal=True,
            )
            rgb = temp["colors"][color_name]
            hex_c = "#%02x%02x%02x" % rgb

            html = f"""
            <div style="
                max-width:260px;
                aspect-ratio:1/1.414;
                background:white;
                {temp['border']} {hex_c};
                padding:14px;
                font-family:Arial;
                overflow:hidden;
                box-shadow:0 4px 10px rgba(0,0,0,0.15);
            ">
              <div style="font-weight:bold;">{temp['name']}</div>
              <div style="color:{hex_c};font-size:10px;">{temp['role']}</div>
              <hr>
              <b style="font-size:9px;color:{hex_c}">SUMMARY</b>
              <div style="font-size:8px">{temp['summary']}</div>
              <b style="font-size:9px;color:{hex_c}">SKILLS</b>
              <div style="font-size:8px">{temp['skills']}</div>
              <b style="font-size:9px;color:{hex_c}">EXPERIENCE</b>
              <div style="font-size:8px;white-space:pre-line">{temp['experience']}</div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)

            if st.button(f"Select {temp['type']}", key=f"btn{i}"):
                st.session_state.user_data["color_rgb"] = rgb
                st.session_state.step = 1
                st.rerun()

# ==========================================
# STEP 1 – USER DETAILS
# ==========================================
elif st.session_state.step == 1:
    st.header("📝 Personal Details")

    with st.form("details"):
        name = st.text_input("Full Name")
        role = st.text_input("Job Role")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        city = st.text_input("City")
        country = st.text_input("Country")

        if st.form_submit_button("Next"):
            st.session_state.user_data.update(
                {
                    "name": name,
                    "role": role,
                    "email": email,
                    "phone": phone,
                    "city": city,
                    "country": country,
                }
            )
            st.session_state.step = 2
            st.rerun()

# ==========================================
# STEP 2 – AI CONTENT
# ==========================================
elif st.session_state.step == 2:
    role = st.session_state.user_data["role"]

    if st.button("✨ Generate Skills"):
        st.session_state.user_data["skills"] = get_ai_suggestions(role, "skills")

    skills = st.text_area("Skills", st.session_state.user_data.get("skills", ""))

    if st.button("✨ Generate Summary"):
        st.session_state.user_data["summary"] = get_ai_suggestions(role, "summary", skills)

    summary = st.text_area("Summary", st.session_state.user_data.get("summary", ""))

    exp = st.text_area("Experience")
    edu = st.text_area("Education")
    certs = st.text_area("Certifications")
    projects = st.text_area("Projects")
    achievements = st.text_area("Achievements")

    st.session_state.user_data.update(
        {
            "skills": skills,
            "summary": summary,
            "experience": exp,
            "education": edu,
            "certs": certs,
            "projects": projects,
            "achievements": achievements,
        }
    )

    if st.button("✅ Download PDF"):
        pdf = create_pdf(st.session_state.user_data)
        st.download_button(
            "📥 Download Resume",
            pdf,
            file_name="Resume.pdf",
            mime="application/pdf",
        )
