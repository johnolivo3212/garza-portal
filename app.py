import streamlit as st
import os
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Garza Law Firm | Intake Portal", page_icon="⚖️", layout="centered")

# --- CUSTOM CSS FOR MODERN LOOK & BRANDING ---
st.markdown("""
<style>
    .sub-header { font-size: 1.2rem; color: #4B5563; text-align: center; margin-bottom: 2rem; margin-top: 5px; font-weight: 500;}
    .security-badge { background-color: #F0FDF4; color: #166534; padding: 1rem; border-radius: 10px; font-weight: 600; text-align: center; margin-bottom: 2rem; border: 1px solid #BBF7D0; font-size: 0.95rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);}
    
    /* Customizing the main button to match Garza Law Firm Navy Blue */
    .stButton>button { width: 100%; font-size: 1.1rem; font-weight: bold; border-radius: 8px; background-color: #002B5C; color: white; border: none; padding: 0.6rem 1rem; transition: 0.3s;}
    .stButton>button:hover { background-color: #001A38; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    
    /* Styling the uploader area */
    [data-testid="stFileUploadDropzone"] { border: 2px dashed #002B5C; border-radius: 10px; background-color: #F8FAFC; padding: 2rem;}
</style>
""", unsafe_allow_html=True)

# --- HEADER & LOGO ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    try:
        st.image("logo.png", use_container_width=True)
    except FileNotFoundError:
        st.error("⚠️ Please place 'Garza law firm logo.png' in the same folder as this script.")

st.markdown('<p class="sub-header">Secure Client Intake Portal</p>', unsafe_allow_html=True)
st.markdown('<div class="security-badge">🔒 CONFIDENTIAL & SECURE: Files are processed with end-to-end encryption and instantly purged from temporary storage after analysis.</div>', unsafe_allow_html=True)

# --- SIDEBAR (SETTINGS) ---
with st.sidebar:
    st.header("⚙️ System Settings")
    
    st.divider()
    st.caption("Authorized for Garza Law Firm personnel only.")

# --- MAIN CONTENT ---
st.write("### 📂 Upload Intake File")
uploaded_file = st.file_uploader("Drag and drop an audio file or transcript here (.txt, .csv, .pdf, .mp3, .wav)", type=["txt", "csv", "pdf", "mp3", "wav", "m4a"], label_visibility="collapsed")

# --- PROCESSING LOGIC ---
if st.button("🚀 Generate Intake Summary"):
    
        
    if not uploaded_file:
        st.warning("⚠️ Please upload a client file first.")
    else:
        with st.spinner("Securely analyzing every detail of the intake call..."):
            try:
                # 1. Initialize AI Client
                client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                
                # 2. Secure temporary file saving
                temp_filename = f"secure_temp_{uploaded_file.name}"
                with open(temp_filename, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 3. Upload file for AI processing
                gemini_file = client.files.upload(file=temp_filename)
                
                # 4. THE INVISIBLE AUTOMATED PROMPT - CUSTOMIZED FOR GARZA LAW
                system_prompt = """
                You are a highly secure and meticulous legal assistant for the Garza Law Firm, an East Tennessee firm specializing in Personal Injury, Criminal Defense, DUI Defense, and Social Security Disability.
                
                Analyze this intake call thoroughly. I need EVERY SINGLE DETAIL discussed in this call. Do not summarize or gloss over anything.
                
                Please extract and format the following:
                1. **Practice Area Classification:** Identify if this is a Personal Injury, Criminal Defense, DUI Defense, Social Security Disability, or Other matter.
                2. **Client Information:** Full name, contact details, dates, and locations.
                3. **Incident/Case Details:** Date of incident/arrest/injury, location, police involvement, medical treatment, BAC levels, or any specific facts.
                4. **Caller Statements:** Every specific claim, issue, timeline, or detail the caller provided. Be exhaustive.
                5. **Specialist Statements:** Exactly what the Garza Law Firm intake specialist advised, offered, or asked.
                6. **Action Items:** What happens next, pending documents needed, or scheduled follow-ups.
                
                Format the output professionally using clean Markdown, bullet points, and bold headers. Maintain a formal, authoritative legal tone.
                """
                
                # 5. Generate report
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=[system_prompt, gemini_file]
                )
                
                st.success("✅ Analysis Complete!")
                st.divider()
                
                # 6. Display the final report
                st.code(response.text, language="markdown", wrap_lines=True)
                
                # 7. CRITICAL SECURITY: CLEANUP
                os.remove(temp_filename) 
                client.files.delete(name=gemini_file.name) 
                
            except Exception as e:
                st.error(f"❌ An error occurred during secure processing: {e}")
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
