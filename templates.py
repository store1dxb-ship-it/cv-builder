# templates.py

template1 = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: A4; margin: 0; }
        body { font-family: 'Helvetica', sans-serif; padding: 40px; color: #333; }
        .header { border-bottom: 2px solid #2c3e50; padding-bottom: 10px; margin-bottom: 20px; }
        .name { font-size: 32px; font-weight: bold; color: #2c3e50; text-transform: uppercase; }
        .role { font-size: 18px; color: #7f8c8d; }
        h3 { color: #2c3e50; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 25px; }
        p { white-space: pre-line; } /* Maintains line breaks from text area */
    </style>
</head>
<body>
    <div class="header">
        <div class="name">{{ name }}</div>
        <div class="role">{{ role }}</div>
        <div>{{ email }} | {{ phone }}</div>
    </div>
    <h3>Professional Summary</h3>
    <p>{{ summary }}</p>
    
    <h3>Experience</h3>
    <p>{{ experience }}</p>
    
    <h3>Education</h3>
    <p>{{ education }}</p>
</body>
</html>
"""

template2 = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: A4; margin: 0; }
        body { font-family: 'Times New Roman', serif; padding: 50px; }
        .center { text-align: center; }
        .name { font-size: 36px; text-transform: uppercase; }
        h3 { text-transform: uppercase; border-bottom: 1px solid #000; font-size: 14px; margin-top: 20px; }
        p { white-space: pre-line; }
    </style>
</head>
<body>
    <div class="center">
        <div class="name">{{ name }}</div>
        <div>{{ role }} &bull; {{ phone }} &bull; {{ email }}</div>
    </div>
    <h3>Profile</h3>
    <p>{{ summary }}</p>
    <h3>Work History</h3>
    <p>{{ experience }}</p>
    <h3>Education</h3>
    <p>{{ education }}</p>
</body>
</html>
"""

template3 = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: A4; margin: 0; }
        body { font-family: sans-serif; margin: 0; display: flex; height: 100vh; }
        .sidebar { width: 30%; background: #27ae60; color: white; padding: 20px; height: 100%; box-sizing: border-box; }
        .main { width: 70%; padding: 20px; }
        .name { font-size: 35px; color: #27ae60; font-weight: bold; }
        h3 { color: #333; border-bottom: 2px solid #27ae60; }
        p { white-space: pre-line; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h3>CONTACT</h3>
        <p>{{ phone }}<br>{{ email }}</p>
        <br>
        <h3>ROLE</h3>
        <p>{{ role }}</p>
    </div>
    <div class="main">
        <div class="name">{{ name }}</div>
        <hr>
        <h3>SUMMARY</h3>
        <p>{{ summary }}</p>
        <h3>EXPERIENCE</h3>
        <p>{{ experience }}</p>
        <h3>EDUCATION</h3>
        <p>{{ education }}</p>
    </div>
</body>
</html>
"""

template4 = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: A4; margin: 0; }
        body { font-family: Arial, sans-serif; margin: 0; }
        .banner { background: #c0392b; color: white; padding: 30px; }
        .name { font-size: 40px; font-weight: bold; }
        .content { padding: 30px; }
        h3 { color: #c0392b; font-weight: bold; }
        p { white-space: pre-line; }
    </style>
</head>
<body>
    <div class="banner">
        <div class="name">{{ name }}</div>
        <div>{{ role }}</div>
        <div style="margin-top: 10px; font-size: 12px;">{{ email }} | {{ phone }}</div>
    </div>
    <div class="content">
        <h3>SUMMARY</h3>
        <p>{{ summary }}</p>
        <h3>EXPERIENCE</h3>
        <p>{{ experience }}</p>
        <h3>EDUCATION</h3>
        <p>{{ education }}</p>
    </div>
</body>
</html>
"""

template5 = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page { size: A4; margin: 0; }
        body { font-family: Verdana, sans-serif; display: flex; height: 100vh; margin: 0; }
        .left { width: 65%; padding: 30px; }
        .right { width: 35%; background: #f4ecf7; border-left: 5px solid #8e44ad; padding: 30px; height: 100%; box-sizing: border-box; }
        .name { color: #8e44ad; font-size: 30px; font-weight: bold; }
        h3 { background: #8e44ad; color: white; padding: 5px; display: inline-block; font-size: 14px; }
        p { white-space: pre-line; }
    </style>
</head>
<body>
    <div class="left">
        <div class="name">{{ name }}</div>
        <div>{{ role }}</div>
        <br>
        <h3>EXPERIENCE</h3>
        <p>{{ experience }}</p>
    </div>
    <div class="right">
        <h3>CONTACT</h3>
        <p>{{ email }}<br>{{ phone }}</p>
        <h3>EDUCATION</h3>
        <p>{{ education }}</p>
        <h3>SUMMARY</h3>
        <p style="font-size: 12px;">{{ summary }}</p>
    </div>
</body>
</html>
"""

# Export dictionary
all_templates = {
    "Classic Blue": template1,
    "Modern Minimal": template2,
    "Green Sidebar": template3,
    "Bold Red": template4,
    "Creative Purple": template5
}
