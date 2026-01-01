import streamlit as st

# ===== Step 1: Page Config =====
st.set_page_config(page_title="CV Builder", layout="centered")

st.title("📝 Interactive CV Builder")

# ===== Step 2: User Input =====
st.header("Step 1: Enter Your Information")

name = st.text_input("Full Name")
email = st.text_input("Email Address")
phone = st.text_input("Phone Number")
address = st.text_input("Address")
linkedin = st.text_input("LinkedIn URL")
github = st.text_input("GitHub URL")
summary = st.text_area("Professional Summary")
education = st.text_area("Education (Degree, College, Year)")
experience = st.text_area("Work Experience")
skills = st.text_area("Skills (Comma separated)")

# ===== Step 3: Select Template =====
st.header("Step 2: Select a Template")

templates = ["Classic", "Modern", "Creative"]
selected_template = st.selectbox("Choose Template", templates)

# ===== Step 4: Generate CV =====
st.header("Step 3: Preview CV")

if st.button("Generate CV"):
    st.subheader(f"CV - {selected_template} Template")
    
    st.markdown(f"""
**Name:** {name}  
**Email:** {email}  
**Phone:** {phone}  
**Address:** {address}  
**LinkedIn:** {linkedin}  
**GitHub:** {github}  

**Summary:**  
{summary}

**Education:**  
{education}

**Experience:**  
{experience}

**Skills:**  
{skills}
""")

    st.success("✅ CV Generated Successfully! You can now copy or screenshot it.")
