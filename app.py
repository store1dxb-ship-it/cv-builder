# Is line ko file ke sabse upar (Imports section mein) add karein:
from st_click_detector import click_detector

# ... (Step 1 and Step 2 code remains SAME) ...

# --- STEP 3: TEMPLATE SELECTION (CLICKABLE THUMBNAILS) ---
elif st.session_state.step == 3:
    st.header("🏆 Step 3: Choose Your Professional Template")
    
    # Initialize selection
    if 'selected_template' not in st.session_state:
        st.session_state.selected_template = "Classic Blue"

    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.subheader("🎨 Select Design")
        
        # --- CSS STYLES ---
        css_content = """
            .thumb-box {
                width: 100%; min-height: 150px; border: 1px solid #ddd;
                border-radius: 8px; margin-bottom: 15px; background: white;
                overflow: hidden; cursor: pointer; position: relative;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: all 0.2s;
            }
            .thumb-box:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            
            /* Selected State Highlight */
            .selected-img { border: 3px solid #007bff; transform: scale(1.02); }
            
            /* Text Styles */
            .t-name { font-weight: bold; font-size: 10px; margin-bottom: 3px; }
            .t-role { font-size: 8px; color: #555; margin-bottom: 5px; }
            .t-text { font-size: 6px; color: #666; line-height: 1.3; margin-bottom: 4px; }
            .t-head { font-weight: bold; font-size: 7px; margin-top: 6px; margin-bottom: 3px; text-transform: uppercase; }
            
            /* Specific Styles */
            .tb-header { border-bottom: 3px solid #2c3e50; padding: 8px; background: #f8f9fa; }
            .tm-box { padding: 12px; text-align: center; } .tm-line { border-bottom: 1px solid #333; margin: 6px 30%; }
            .tg-container { display: flex; height: 100%; min-height: 150px; } .tg-left { width: 32%; background: #27ae60; padding: 8px; color: white; } .tg-right { width: 68%; padding: 8px; }
            .tr-header { background: #c0392b; color: white; padding: 12px; }
            .tp-container { display: flex; height: 100%; min-height: 150px; } .tp-left { width: 65%; padding: 10px; } .tp-right { width: 35%; background: #f4ecf7; border-left: 3px solid #8e44ad; padding: 10px; }
        """

        # --- HTML BUILDER FOR THUMBNAILS ---
        # Hum check karenge ki kaunsa selected hai taaki uspar Border laga sakein
        sel = st.session_state.selected_template
        
        # Helper to add 'selected-img' class
        def get_class(name):
            return "thumb-box selected-img" if sel == name else "thumb-box"

        html_code = f"""
        <div id='Classic Blue' class='{get_class("Classic Blue")}'>
            <div class='tb-header'><div class='t-name' style='color:#2c3e50'>VIKRAM MALHOTRA</div><div class='t-role'>Senior Engineer</div></div>
            <div style='padding:8px'><div class='t-head' style='color:#2c3e50'>SUMMARY</div><div class='t-text'>Results-oriented professional...</div></div>
        </div>

        <div id='Modern Minimal' class='{get_class("Modern Minimal")}'>
            <div class='tm-box'>
                <div class='t-name' style='font-family:serif; font-size:12px;'>ADITI SHARMA</div><div class='t-role'>Digital Marketing</div>
                <div class='tm-line'></div><div style='text-align:left; margin-top:8px;'><div class='t-head'>PROFILE</div><div class='t-text'>Creative marketer...</div></div>
            </div>
        </div>

        <div id='Green Sidebar' class='{get_class("Green Sidebar")}'>
            <div class='tg-container'>
                <div class='tg-left'><div style='font-size:6px; color:white'>Contact<br>Skills</div></div>
                <div class='tg-right'><div class='t-name' style='color:#27ae60'>RAHUL VERMA</div><div class='t-head'>SUMMARY</div><div class='t-text'>Data Scientist...</div></div>
            </div>
        </div>

        <div id='Bold Red' class='{get_class("Bold Red")}'>
            <div class='tr-header'><div class='t-name' style='color:white'>ANJALI KAPOOR</div></div>
            <div style='padding:10px'><div class='t-head' style='color:#c0392b'>SUMMARY</div><div class='t-text'>HR professional...</div></div>
        </div>

        <div id='Creative Purple' class='{get_class("Creative Purple")}'>
            <div class='tp-container'>
                <div class='tp-left'><div class='t-name' style='color:#8e44ad'>KARTIK REDDY</div><div class='t-head' style='background:#8e44ad; color:white;'>EXPERIENCE</div></div>
                <div class='tp-right'><div class='t-head'>CONTACT</div></div>
            </div>
        </div>
        """

        # --- CLICK DETECTOR (Magic happens here) ---
        # Yeh function HTML render karega aur click hone par ID return karega
        clicked_id = click_detector(html_code, css_content)

        # Agar user ne click kiya, toh state update karein aur rerun karein
        if clicked_id and clicked_id != st.session_state.selected_template:
            st.session_state.selected_template = clicked_id
            st.rerun()
            
        st.divider()
        if st.button("⬅️ Edit Data", key="back_btn"):
            st.session_state.step = 2
            st.rerun()

    with col_right:
        st.success(f"✅ Selected Style: **{st.session_state.selected_template}**")
        st.subheader("Live Preview (Full Size)")
        
        # --- GENERATE & PREVIEW ---
        html_template_string = templates.all_templates[st.session_state.selected_template]
        jinja_template = Template(html_template_string)
        filled_html = jinja_template.render(**st.session_state.user_data)
        
        # Force White Background in Preview
        preview_html = f"<style>body {{ background-color: white !important; }}</style>{filled_html}"
        st.components.v1.html(preview_html, height=800, scrolling=True)
        
        # --- DOWNLOAD BUTTON ---
        pdf_bytes = HTML(string=filled_html).write_pdf()
        
        st.download_button(
            label=f"⬇️ Download {st.session_state.selected_template} PDF",
            data=pdf_bytes,
            file_name=f"{st.session_state.user_data.get('name', 'Resume')}.pdf",
            mime="application/pdf",
            type="primary"
        )
        
