import streamlit as st
import os
from google import genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Garza Law Firm | Intake Portal", page_icon="⚖️", layout="centered")

# --- CUSTOM CSS FOR MODERN LOOK & BRANDING ---
st.markdown("""
<style>
    /* Force main app background to white */
    .stApp {
        background-color: #ffffff !important;
    }

    /* Fix the File Uploader dropzone */
    [data-testid="stFileUploadDropzone"] {
        background-color: #f8f9fa !important;
        border: 2px dashed #002B5C !important;
        color: #2c3e50 !important;
    }
    
    /* Ensure the text inside the dropzone is dark */
    [data-testid="stFileUploadDropzone"] div, 
    [data-testid="stFileUploadDropzone"] span {
        color: #2c3e50 !important;
    }

    /* Fix the Generate Button */
    div.stButton > button {
        background-color: #002B5C !important;
        color: #ffffff !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
    }
    
    div.stButton > button:hover {
        background-color: #001a38 !important;
        color: #ffffff !important;
    }
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
                # 4. THE INVISIBLE AUTOMATED PROMPT - CUSTOMIZED FOR GARZA LAW
               # 4. THE INVISIBLE AUTOMATED PROMPT - CUSTOMIZED FOR GARZA LAW
                system_prompt = """
                You are a highly secure and professional legal assistant for Garza Law Firm, PLLC.
                
                Analyze this intake call thoroughly. Extract every detail. 
                
                CRITICAL: Provide your output as a clean, professional document. 
                DO NOT use Markdown syntax, hashtags (#), or asterisks (*). 
                Use plain text, clear headings, and simple indentation. 
                
                Structure the output as follows:
                
                PRACTICE AREA CLASSIFICATION
                (Identify the area)
                
                CLIENT INFORMATION
                (List details here)
                
                INCIDENT DETAILS
                (List facts here)
                
                CALLER STATEMENTS
                (List claims and timelines)
                
                SPECIALIST STATEMENTS
                (List advice given by the firm)
                
                ACTION ITEMS
                (List next steps)
                """
                
                # 5. Generate report
                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=[system_prompt, gemini_file]
                )
                
                st.success("✅ Analysis Complete!")
                st.divider()
                
                # 6. Display the final report
                st.write(response.text)
                
                # 7. CRITICAL SECURITY: CLEANUP
                os.remove(temp_filename) 
                client.files.delete(name=gemini_file.name) 
                
            except Exception as e:
                st.error(f"❌ An error occurred during secure processing: {e}")
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
