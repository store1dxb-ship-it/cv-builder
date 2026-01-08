import streamlit as st
from fpdf import FPDF
import requests
from templates import TEMPLATES

# =========================
# AI CONFIG
# =========================
def get_ai_suggestions(role, info_type):
    api_key = "AIzaSyDGnsQfMEkIb-KloUGVYxGLX4hc80HfdMg"
    model = "gemini-2.5-flash-lite"
    url = f"https://generativelanguage.googleapis.com/v1/models/{model}:generateContent?key={api_key}"

    prompt = f"Write a professional resume summary for a {role}."
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        res = requests.post(url, json=data, timeout=10)
        if res.status_code == 200:
            return res.json()['candidates'][0]['content']['parts'][0]['text']
    except:
        pass
    return ""

# =========================
# PDF LOGIC
# =========================
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "RESUME", ln=True, align="C")
        self.ln(5)

def create_pdf(data):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, data['name'], ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"{data['email']} | {data['phone']}", ln=True)
    pdf.cell(0, 8, data['role'], ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "SUMMARY", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 7, data['summary'])

    return pdf.output(dest="S").encode("latin-1")

# =========================
# STREAMLIT SETUP
# =========================
st.set_page_config(layout="wide", page_title="AI Resume Builder")

if "step" not in st.session_state:
    st.session_state.step = 1

if "data" not in st.session_state:
    st.session_state.data = {}

if "template" not in st.session_state:
    st.session_state.template = "Classic"

st.title("🚀 AI Resume Builder")

# =========================
# STEP 1
# =========================
if st.session_state.step == 1:
    st.header("Step 1: Personal Details")

    with st.form("form1"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        role = st.text_input("Target Job Role")

        if st.form_submit_button("Next"):
            st.session_state.data.update({
                "name": name,
                "email": email,
                "phone": phone,
                "role": role
            })
            st.session_state.step = 2
            st.rerun()

# =========================
# STEP 2
# =========================
elif st.session_state.step == 2:
    st.header("Step 2: AI + Templates")

    col1, col2 = st.columns([1,2])

    # LEFT: TEMPLATE THUMBNAILS
    with col1:
        st.subheader("Choose Template")

        for name, func in TEMPLATES.items():
            st.markdown(func(st.session_state.data, small=True), unsafe_allow_html=True)
            if st.button(f"Use {name}"):
                st.session_state.template = name

    # RIGHT: LIVE PREVIEW + AI
    with col2:
        st.subheader("Live Preview")

        if st.button("✨ Generate AI Summary"):
            with st.spinner("AI is writing..."):
                st.session_state.data["summary"] = get_ai_suggestions(
                    st.session_state.data["role"], "summary"
                )

        st.session_state.data["summary"] = st.text_area(
            "Edit Summary",
            st.session_state.data.get("summary",""),
            height=150
        )

        preview_func = TEMPLATES[st.session_state.template]
        st.markdown(preview_func(st.session_state.data), unsafe_allow_html=True)

        if st.button("📄 Download PDF"):
            pdf = create_pdf(st.session_state.data)
            st.download_button(
                "Click to Download",
                pdf,
                "Resume.pdf",
                "application/pdf"
            )
