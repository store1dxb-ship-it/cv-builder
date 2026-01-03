import streamlit as st
from fpdf import FPDF
from google import genai

# ================= AI CONFIG (NEW SDK) =================
client = genai.Client(
    api_key="AIzaSyBnzIDq_M918jBKRIerScQfOefHDO9J-VM"
)

MODEL = "gemini-2.0-flash"   # ✅ CURRENTLY SUPPORTED


def get_ai_suggestions(role, info_type="summary"):
    try:
        if info_type == "summary":
            prompt = f"Write a professional 2–3 line ATS-friendly resume summary for a {role}."
        else:
            prompt = f"Write 4 strong resume bullet points for work experience of a {role}."

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        return f"AI ERROR: {str(e)}"


# ================= PAGE CONFIG =================
st.set_page_config(page_title="AI CV Builder", layout="wide")

if "step" not in st.session_state:
    st.session_state.step = 1
if "user_data" not in st.session_state:
    st.session_state.user_data = {}


# ================= PDF GENERATOR =================
def create_pdf(data):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 22)
    pdf.cell(0, 15, data["name"], ln=True)
    pdf.line(10, 25, 200, 25)

    pdf.ln(8)
    pdf.set_font("Arial", "", 11)

    sections = [
        ("Summary", data.get("summary")),
        ("Experience", data.get("experience")),
        ("Education", data.get("education")),
        ("Skills", data.get("skills")),
    ]

    for title, content in sections:
        if content:
            pdf.set_font("Arial", "B", 13)
            pdf.cell(0, 10, title.upper(), ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 7, content)
            pdf.ln(3)

    return pdf.output(dest="S").encode("latin-1")


# ================= UI FLOW =================
if st.session_state.step == 1:
    st.title("👤 Step 1: Personal Details")

    st.session_state.user_data["name"] = st.text_input("Full Name")
    st.session_state.user_data["role"] = st.text_input("Target Job Role")

    if st.button("Next ➡️"):
        if st.session_state.user_data["name"] and st.session_state.user_data["role"]:
            st.session_state.step = 2
            st.rerun()
        else:
            st.error("Please fill all fields")


elif st.session_state.step == 2:
    st.title("🤖 Step 2: AI Suggestions")

    role = st.session_state.user_data["role"]

    col1, col2 = st.columns(2)

    with col1:
        if st.button("✨ Generate Summary"):
            with st.spinner("Generating summary..."):
                st.session_state.user_data["summary"] = get_ai_suggestions(role, "summary")

    with col2:
        if st.button("✨ Generate Experience"):
            with st.spinner("Generating experience..."):
                st.session_state.user_data["experience"] = get_ai_suggestions(role, "exp")

    summary = st.text_area("Summary", st.session_state.user_data.get("summary", ""), height=120)
    experience = st.text_area("Experience", st.session_state.user_data.get("experience", ""), height=180)

    if st.button("Next ➡️"):
        st.session_state.user_data.update({
            "summary": summary,
            "experience": experience
        })
        st.session_state.step = 3
        st.rerun()


elif st.session_state.step == 3:
    st.title("🎓 Step 3: Education & Skills")

    education = st.text_area("Education")
    skills = st.text_area("Skills")

    if st.button("Generate CV ✅"):
        st.session_state.user_data.update({
            "education": education,
            "skills": skills
        })
        st.session_state.step = 4
        st.rerun()


elif st.session_state.step == 4:
    st.title("✅ Your Resume is Ready")

    pdf_bytes = create_pdf(st.session_state.user_data)

    st.download_button(
        "📥 Download Resume PDF",
        data=pdf_bytes,
        file_name="ATS_Resume.pdf",
        use_container_width=True
    )

    if st.button("Create New Resume 🔄"):
        st.session_state.step = 1
        st.session_state.user_data = {}
        st.rerun()
