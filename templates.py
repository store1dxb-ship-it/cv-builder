def template_one(data, small=False):
    title = "20px" if small else "32px"
    body = "12px" if small else "15px"

    return f"""
    <div style="border:1px solid #ccc;padding:10px">
        <h2 style="font-size:{title};margin:0">{data.get('name','')}</h2>
        <p style="font-size:{body}">{data.get('email','')} | {data.get('phone','')}</p>
        <hr>
        <b>Professional Summary</b>
        <p>{data.get('summary','')}</p>
    </div>
    """

def template_two(data, small=False):
    title = "20px" if small else "30px"

    return f"""
    <div style="background:#f4f4f4;padding:10px">
        <h2 style="color:#8b0000;font-size:{title}">{data.get('name','')}</h2>
        <p><i>{data.get('role','')}</i></p>
        <p>{data.get('summary','')}</p>
    </div>
    """

TEMPLATES = {
    "Classic": template_one,
    "Modern": template_two
}
