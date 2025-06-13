import streamlit as st
import pytesseract
from PIL import Image
import tempfile
import pdf2image
import base64
import openai
import langdetect
import docx
import urllib.parse

# Initialize states
if "chat_visible" not in st.session_state:
    st.session_state["chat_visible"] = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Page Config ---
st.set_page_config(
    page_title="AI Legal Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Enhanced Custom CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main {
    padding: 0 !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Main app styling */
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem 2rem;
    border-radius: 20px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
    box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}

.app-header h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.app-header p {
    font-size: 1.2rem;
    opacity: 0.9;
    font-weight: 300;
}

.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
    border: 1px solid #e1e8ed;
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.feature-card h3 {
    color: #2c3e50;
    margin-bottom: 1rem;
    font-weight: 600;
}

.upload-section {
    background: linear-gradient(145deg, #f8f9fa, #e9ecef);
    padding: 2rem;
    border-radius: 16px;
    border: 2px dashed #6c757d;
    text-align: center;
    margin-bottom: 2rem;
}

.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.8rem 2rem;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
}

.stTextInput > div > div > input,
.stTextArea > div > textarea {
    border-radius: 12px;
    border: 2px solid #e1e8ed;
    padding: 1rem;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Floating Chat Button */
.chat-float-button {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 28px;
    cursor: pointer;
    z-index: 9999;
    box-shadow: 0 8px 32px rgba(79, 70, 229, 0.4);
    transition: all 0.3s ease;
    border: none;
}

.chat-float-button:hover {
    transform: scale(1.1);
    box-shadow: 0 12px 40px rgba(79, 70, 229, 0.6);
}

#floating-chat-btn {
    position: fixed;
    bottom: 32px;
    right: 32px;
    z-index: 9999;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 64px;
    height: 64px;
    font-size: 2rem;
    box-shadow: 0 4px 24px #0003;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}
#floating-chat-btn:hover {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}

/* Modern Chat Container */
.chat-container {
    position: fixed;
    bottom: 120px;
    right: 30px;
    width: 380px;
    height: 550px;
    background: white;
    border-radius: 24px;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.15);
    z-index: 9998;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(20px);
    animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chat-header {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-weight: 600;
    font-size: 16px;
}

.chat-header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.chat-status-dot {
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.chat-close-btn {
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.chat-close-btn:hover {
    background: rgba(255, 255, 255, 0.3);
    transform: scale(1.1);
}

.chat-messages {
    flex: 1;
    padding: 20px;
    overflow-y: auto;
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.chat-messages::-webkit-scrollbar {
    width: 4px;
}

.chat-messages::-webkit-scrollbar-track {
    background: transparent;
}

.chat-messages::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.5);
    border-radius: 2px;
}

/* Modern Message Bubbles */
.user-message {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    gap: 8px;
}

.bot-message {
    display: flex;
    justify-content: flex-start;
    align-items: flex-end;
    gap: 8px;
}

.message-bubble {
    max-width: 75%;
    padding: 12px 16px;
    border-radius: 20px;
    font-size: 14px;
    line-height: 1.4;
    word-wrap: break-word;
    position: relative;
}

.user-bubble {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    border-bottom-right-radius: 8px;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
}

.bot-bubble {
    background: white;
    color: #374151;
    border: 1px solid #e5e7eb;
    border-bottom-left-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.message-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}

.bot-avatar {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
}

.message-time {
    font-size: 11px;
    color: #9ca3af;
    margin-top: 4px;
    text-align: center;
}

/* Chat Input */
.chat-input-container {
    padding: 20px;
    background: white;
    border-top: 1px solid #e5e7eb;
    display: flex;
    gap: 12px;
    align-items: flex-end;
}

.chat-input {
    flex: 1;
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 12px 16px;
    font-size: 14px;
    resize: none;
    outline: none;
    transition: all 0.2s ease;
    max-height: 80px;
    min-height: 44px;
}

.chat-input:focus {
    border-color: #4f46e5;
    background: white;
    box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1);
}

.chat-send-btn {
    width: 44px;
    height: 44px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    border: none;
    border-radius: 50%;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 16px;
}

.chat-send-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
}

.chat-send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Typing indicator */
.typing-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    border-bottom-left-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    max-width: 80px;
}

.typing-dots {
    display: flex;
    gap: 4px;
}

.typing-dot {
    width: 6px;
    height: 6px;
    background: #9ca3af;
    border-radius: 50%;
    animation: typing 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
    0%, 80%, 100% { transform: scale(0.8); opacity: 0.5; }
    40% { transform: scale(1); opacity: 1; }
}

/* Welcome message */
.chat-welcome {
    text-align: center;
    padding: 20px;
    color: #6b7280;
    font-size: 14px;
}

.welcome-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
}

.sidebar-content {
    padding: 2rem 1rem;
}

.sidebar-logo {
    text-align: center;
    margin-bottom: 2rem;
}

/* Success/Error messages */
.stSuccess {
    background: linear-gradient(135deg, #00d4aa, #00b09b);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    border: none;
}

.stError {
    background: linear-gradient(135deg, #ff6b6b, #ee5a52);
    color: white;
    border-radius: 12px;
    padding: 1rem;
    border: none;
}

/* Hide default streamlit elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Responsive design */
@media (max-width: 768px) {
    .chat-container {
        width: calc(100vw - 40px);
        right: 20px;
        left: 20px;
        height: 70vh;
        bottom: 100px;
    }

    .chat-float-button {
        width: 60px;
        height: 60px;
        font-size: 24px;
    }
}

/* Hide Streamlit's default chat button styling */
div[data-testid="column"]:last-child {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# --- API Setup ---
try:
    openai.api_key = st.secrets["OPENROUTER_API_KEY"]
    openai.api_base = "https://openrouter.ai/api/v1"
except:
    st.error("⚠️ OpenRouter API key not found. Please add it to your Streamlit secrets.")

# --- Beautiful Black Sidebar Styling ---
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background: #111827 !important;
        color: #fff;
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        min-width: 270px;
        max-width: 320px;
    }
    .sidebar-logo {
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar-logo img {
        width: 60px;
        border-radius: 16px;
        margin-bottom: 0.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    .sidebar-title {
        font-size: 1.5rem;
        font-weight: 700;
        letter-spacing: 1px;
        color: #fff;
        margin-bottom: 0.5rem;
    }
    .sidebar-desc {
        font-size: 1rem;
        color: #a5b4fc;
        margin-bottom: 1.5rem;
    }
    .sidebar-section {
        font-size: 1.1rem;
        font-weight: 600;
        color: #a5b4fc;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        letter-spacing: 0.5px;
    }
    .sidebar-link {
        display: block;
        color: #fff;
        background: rgba(255,255,255,0.08);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.5rem;
        text-decoration: none;
        transition: background 0.2s;
        font-weight: 500;
    }
    .sidebar-link:hover {
        background: #374151;
        color: #fff;
        text-decoration: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Content ---
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-logo">
            <img src="https://img.icons8.com/color/96/000000/law.png" alt="LegalBot Logo">
            <div class="sidebar-title">AI Legal Assistant</div>
            <div class="sidebar-desc">Your smart legal helper</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('<div class="sidebar-section">Features</div>', unsafe_allow_html=True)
    st.markdown("""
        <div style="margin-bottom:1rem;">
            <div class="sidebar-link" style="margin-bottom:8px;">
                <b>📁 Document Upload</b>
            </div>
            <div class="sidebar-link" style="margin-bottom:8px;">
                <b>🔍 Text Extraction</b> 
            </div>
            <div class="sidebar-link" style="margin-bottom:8px;">
                <b>🌐 Document Translation</b>
            </div>
            <div class="sidebar-link" style="margin-bottom:8px;">
                <b>📝 Summarize</b>
            </div>
            <div class="sidebar-link" style="margin-bottom:8px;">
                <b>❓ Ask Question</b>
            </div>
            <div class="sidebar-link">
                <b>🤖 Chatbot</b>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section">Resources</div>', unsafe_allow_html=True)
    st.markdown("""
        <a class="sidebar-link resource-link" href="https://indiacode.nic.in/" target="_blank">
            <span style="font-size:1.2em;vertical-align:middle;">📚</span>
            <span style="margin-left:8px;vertical-align:middle;">Indian Law Codes</span>
        </a>
        <a class="sidebar-link resource-link" href="https://www.supremecourtofindia.nic.in/" target="_blank">
            <span style="font-size:1.2em;vertical-align:middle;">⚖️</span>
            <span style="margin-left:8px;vertical-align:middle;">Supreme Court</span>
        </a>
    """, unsafe_allow_html=True)
    st.markdown('<div style="margin-top:2rem;font-size:0.95rem;color:#a5b4fc;">Made with ❤️ by Edunet Foundation</div>', unsafe_allow_html=True)

# Add this to your sidebar CSS (if not already present)
st.markdown("""
    <style>
    .resource-link {
        display: flex !important;
        align-items: center;
        gap: 8px;
        background: linear-gradient(90deg, #232946 0%, #3730a3 100%);
        color: #fff !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
        font-size: 1rem;
        text-decoration: none !important;
        box-shadow: 0 2px 8px rgba(36, 37, 47, 0.08);
        transition: background 0.2s, box-shadow 0.2s;
    }
    .resource-link:hover {
        background: linear-gradient(90deg, #3730a3 0%, #232946 100%);
        color: #a5b4fc !important;
        box-shadow: 0 4px 16px rgba(79, 70, 229, 0.18);
        text-decoration: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def extract_text_from_image(image_file):
    return pytesseract.image_to_string(Image.open(image_file))


def extract_text_from_pdf(pdf_file):
    with tempfile.TemporaryDirectory() as path:
        images = pdf2image.convert_from_bytes(pdf_file.read(), dpi=300, output_folder=path)
        return "".join([pytesseract.image_to_string(img) for img in images])


def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])


def translate_to_english(text):
    try:
        lang = langdetect.detect(text)
        if lang != 'en':
            prompt = f"Translate this to English:\n{text}"
            response = openai.ChatCompletion.create(
                model="mistralai/mistral-7b-instruct",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content, lang
        return text, 'en'
    except Exception as e:
        return f"Translation Error: {e}", 'error'


def summarize_text(text):
    try:
        prompt = f"Provide a comprehensive legal summary of the following document:\n{text}"
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def answer_question(text, question):
    try:
        prompt = f"Based on this legal document:\n{text}\n\nPlease answer this question: {question}"
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def create_download_link(text, filename="legal_summary.txt"):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 10px 20px; text-decoration: none; border-radius: 8px; display: inline-block; margin: 10px 0;">📥 Download Summary</a>'


def generate_share_links(text):
    encoded = urllib.parse.quote(text[:300] + "...")
    email = f"mailto:?subject=Legal%20Document%20Summary&body={encoded}"
    whatsapp = f"https://wa.me/?text={encoded}"
    telegram = f"https://t.me/share/url?url=https://&text={encoded}"
    return email, whatsapp, telegram

def chat_ai_response(message):
    try:
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": "..."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"AI API Error: {e}")
        return "I apologize, but I'm having trouble connecting to the AI service right now. Please try again later."


# --- Main App ---
# Header
st.markdown("""
<div class="app-header">
    <h1>⚖️ AI Legal Assistant</h1>
    <p>Powered by Advanced AI • Extract, Analyze, and Understand Legal Documents</p>
</div>
""", unsafe_allow_html=True)

# Main content - Single column layout
st.markdown("### 📁 Document Upload & Processing")

uploaded_file = st.file_uploader(
    "Upload your legal document",
    type=["pdf", "png", "jpg", "jpeg", "txt", "docx"],
    help="Supported formats: PDF, Images (PNG, JPG), Word Documents, Text files"
)

if uploaded_file:
    with st.spinner("🔄 Processing document..."):
        file_type = uploaded_file.type

        if "pdf" in file_type:
            extracted = extract_text_from_pdf(uploaded_file)
        elif "image" in file_type:
            extracted = extract_text_from_image(uploaded_file)
        elif "word" in file_type or uploaded_file.name.endswith(".docx"):
            extracted = extract_text_from_docx(uploaded_file)
        elif "text" in file_type:
            extracted = uploaded_file.read().decode("utf-8")
        else:
            extracted = "Unsupported file format."

    st.success(f"✅ Successfully extracted text from {uploaded_file.name}")

    # Translation if needed
    translated_text, lang = translate_to_english(extracted)
    display_text = translated_text if lang != 'en' else extracted

    if lang != 'en' and lang != 'error':
        st.info(f"🌍 Document translated from {lang.upper()} to English")

    # Display extracted text
    st.markdown("### 📄 Extracted Content")
    st.text_area("Document text", display_text, height=300, key="extracted_text")

    # Action buttons
    col1, col2 = st.columns([2, 3])  # Adjust the ratio for your preferred widths

    with col1:
        generate_summary = st.button("🧠 Generate Summary", use_container_width=True)
    with col2:
        question = st.text_input("💬 Ask about this document", placeholder="Ex: What are the terms?")

    if generate_summary:
        with st.spinner("🤔 Analyzing document..."):
            summary = summarize_text(display_text)
        st.markdown("### 📋 Legal Summary")
        st.write(summary)

        # Download and share options
        st.markdown(create_download_link(summary), unsafe_allow_html=True)

        email_link, wa_link, tg_link = generate_share_links(summary)
        st.markdown(f"""
        <div style="margin-top: 1rem;">
            <a href="{email_link}" style="margin-right: 10px;">📧 Email</a>
            <a href="{wa_link}" style="margin-right: 10px;">💬 WhatsApp</a>
            <a href="{tg_link}">✈️ Telegram</a>
        </div>
        """, unsafe_allow_html=True)

    if question:
        with st.spinner("🔍 Finding answer..."):
            answer = answer_question(display_text, question)
        st.markdown("### 🎯 Answer")
        st.write(f"**Q:** {question}")
        st.write(f"**A:** {answer}")

# --- Floating Chatbot Button & Modal (Bottom Right, Streamlit-native) ---
st.markdown("""
<style>
#floating-chat-btn {
    position: fixed;
    bottom: 32px;
    right: 32px;
    z-index: 9999;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    color: white;
    border: none;
    border-radius: 50%;
    width: 64px;
    height: 64px;
    font-size: 2rem;
    box-shadow: 0 4px 24px #0003;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.2s;
}
#floating-chat-btn:hover {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
}
#floating-chat-modal {
    position: fixed;
    right: 32px;
    bottom: 112px;
    width: 350px;
    max-width: 90vw;
    background: #232946;
    color: #fff;
    border-radius: 16px;
    box-shadow: 0 8px 32px #0005;
    z-index: 10000;
    padding: 1.5rem 1rem 1rem 1rem;
    animation: fadeInUp 0.3s;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(40px);}
    to { opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

if "chat_visible" not in st.session_state:
    st.session_state.chat_visible = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Floating button (Streamlit-native)
float_btn = st.button("Open Chatbot 🤖", key="floating_chat_btn", help="Chat with Legal AI")
if float_btn:
    st.session_state.chat_visible = not st.session_state.chat_visible

# Chat modal (Streamlit-native)
if st.session_state.chat_visible:
    # Display chat history
    for message in st.session_state.chat_history[-8:]:
        if message.get("role") == "user":
            st.markdown(f"<div style='text-align:right;color:#aad;margin-bottom:10px;'>🧑‍💼 <b>You:</b> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='text-align:left;color:#fff;margin-bottom:18px;'>🤖 <b>Bot:</b> {message['content']}</div>", unsafe_allow_html=True)

    def handle_chat_input():
        chat_input = st.session_state.chat_input_modal
        if chat_input:
            with st.spinner("Bot is typing..."):
                bot_response = chat_ai_response(chat_input)  # Call your AI function here
                st.session_state.chat_history.append({"role": "user", "content": chat_input})
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            st.session_state.chat_input_modal = ""

    chat_input = st.text_input("",placeholder="Type your question to the legal bot...",
        label_visibility="collapsed",
        key="chat_input_modal",
        on_change=handle_chat_input
    )
    if st.button("Close Chatbot", key="close_chatbot_btn"):
        st.session_state.chat_visible = False
        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6c757d; border-top: 1px solid #e1e8ed; margin-top: 3rem;">
    <p><strong>AI Legal Assistant</strong></p>
    <p><em>⚠️ This tool provides information only. Always consult with qualified legal professionals for legal advice.</em></p>
</div>
""", unsafe_allow_html=True)
