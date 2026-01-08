import streamlit as st
import requests
from fpdf import FPDF
from templates import TEMPLATES

# ---------------- AI ----------------
def ai_generate(prompt):
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg"
    model = "gemini-2.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"
    data = {"contents":[{"parts":[{"text":prompt}]}]}
    try:
        r = requests.post(url, json=data, timeout=10)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        return ""

# ---------------- ATS ----------------
def ats_score(text, role):
    keywords = role.lower().split()
    hits = sum(1 for k in keywords if k in text.lower())
    return int((hits / max(len(keywords),1)) * 100)

# ---------------- PDF ----------------
class PDF(FPDF):
    def header(self):
        self.set_font("Arial","B",16)
        self.cell(0,10,"RESUME",ln=True,align="C")
        self.ln(5)

def create_pdf(data):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,data['name'],ln=True)
    pdf.set_font("Arial","",12)
    pdf.cell(0,8,data['role'],ln=True)
    pdf.ln(4)

    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"SUMMARY",ln=True)
    pdf.set_font("Arial","",11)
    pdf.multi_cell(0,7,data['summary'])

    pdf.add_page()   # Page 2
    pdf.set_font("Arial","B",14)
    pdf.cell(0,10,"EXPERIENCE",ln=True)
    pdf.set_font("Arial","",11)

    for e in data.get("experience",[]):
        pdf.multi_cell(0,7,
            f"{e['designation']} - {e['company']} ({e['duration']})\n{e['description']}\n"
        )

    return pdf.output(dest="S").encode("latin-1")

# ---------------- STATE ----------------
st.set_page_config(layout="wide")
if "data" not in st.session_state:
    st.session_state.data = {
        "experience": [],
        "skills": [],
        "paid": False
    }
if "template" not in st.session_state:
    st.session_state.template = "Classic"

st.title("🚀 AI Professional Resume Builder")

# ---------------- FORM ----------------
with st.sidebar:
    st.header("Personal & Target")
    st.session_state.data["name"] = st.text_input("Name")
    st.session_state.data["email"] = st.text_input("Email")
    st.session_state.data["phone"] = st.text_input("Phone")
    st.session_state.data["role"] = st.text_input("Target Job")

    if st.button("✨ AI Summary"):
        st.session_state.data["summary"] = ai_generate(
            f"Write resume summary for {st.session_state.data['role']}"
        )

    st.session_state.data["summary"] = st.text_area(
        "Summary", st.session_state.data.get("summary","")
    )

# ---------------- EXPERIENCE ----------------
st.subheader("Professional Experience")

c1,c2,c3 = st.columns(3)
company = c1.text_input("Company")
designation = c2.text_input("Designation")
duration = c3.text_input("Duration")
desc = st.text_area("Description")

if st.button("➕ Add Experience"):
    st.session_state.data["experience"].append({
        "company":company,
        "designation":designation,
        "duration":duration,
        "description":desc
    })

for i,e in enumerate(st.session_state.data["experience"]):
    st.markdown(f"**{e['designation']} – {e['company']}**")
    if st.button("❌ Delete", key=f"del{i}"):
        st.session_state.data["experience"].pop(i)
        st.rerun()

# ---------------- SKILLS ----------------
skills = st.text_input("Skills (comma separated)")
st.session_state.data["skills"] = [s.strip() for s in skills.split(",") if s]

# ---------------- ATS ----------------
full_text = st.session_state.data.get("summary","") + str(st.session_state.data["experience"])
st.metric("ATS Match Score", f"{ats_score(full_text, st.session_state.data.get('role',''))}%")

# ---------------- TEMPLATES ----------------
st.subheader("Templates")
cols = st.columns(4)
i = 0
for name, func in TEMPLATES.items():
    with cols[i % 4]:
        st.markdown(func(st.session_state.data, small=True), unsafe_allow_html=True)
        if st.button(f"Use {name}", key=name):
            st.session_state.template = name
    i += 1

# ---------------- PREVIEW ----------------
st.subheader("Live Preview")
st.markdown(
    TEMPLATES[st.session_state.template](st.session_state.data),
    unsafe_allow_html=True
)

# ---------------- PDF ----------------
if st.button("📄 Download 2-Page PDF"):
    pdf = create_pdf(st.session_state.data)
    st.download_button("Download", pdf, "Resume.pdf", "application/pdf")
