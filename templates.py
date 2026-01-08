def base_template(data, color, locked=False, small=False):
    if locked and not data.get("paid"):
        return """
        <div style="padding:20px;border:2px dashed red">
        🔒 Premium Template<br>Upgrade to Unlock
        </div>
        """

    size = "16px" if small else "30px"

    exp_html = ""
    for e in data.get("experience", []):
        exp_html += f"""
        <p><b>{e['designation']}</b> – {e['company']} ({e['duration']})<br>
        {e['description']}</p>
        """

    return f"""
    <div style="background:#fff;padding:15px;border-top:6px solid {color}">
        <h2 style="color:{color};font-size:{size}">{data.get('name','')}</h2>
        <p>{data.get('role','')}</p>
        <hr>
        <b>Summary</b>
        <p>{data.get('summary','')}</p>
        <b>Experience</b>
        {exp_html}
        <b>Skills</b>
        <p>{", ".join(data.get("skills", []))}</p>
        <b>Education</b>
        <p>{data.get("education","")}</p>
    </div>
    """

TEMPLATES = {
    "Classic": lambda d, s=False: base_template(d, "#333", False, s),
    "Modern": lambda d, s=False: base_template(d, "#8b0000", False, s),
    "Blue": lambda d, s=False: base_template(d, "#004aad", False, s),
    "Green": lambda d, s=False: base_template(d, "#0f7b6c", False, s),
    "Purple": lambda d, s=False: base_template(d, "#5b2d8b", False, s),
    "Executive 🔒": lambda d, s=False: base_template(d, "#000", True, s),
    "Corporate 🔒": lambda d, s=False: base_template(d, "#444", True, s),
    "Minimal 🔒": lambda d, s=False: base_template(d, "#777", True, s),
}
