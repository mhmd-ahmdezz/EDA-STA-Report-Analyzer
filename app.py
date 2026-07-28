import requests
import streamlit as st

# --- Pre-Configured Backend Defaults ---
# Replace 'gsk_your_actual_groq_api_key_here' with your real Groq API key
DEFAULT_NGROK_URL = "https://your-ngrok-url.ngrok-free.dev"
DEFAULT_GROQ_KEY = "gsk_your_groq_api_key_here"

# --- Page Configuration ---
st.set_page_config(
    page_title="EDA STA Report Analyzer",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Modern Theme CSS (Icons Removed) ---
custom_css = """
<style>
    /* Modern Dark Theme Palette */
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: 1px solid #334155;
    }

    /* Headers */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 600;
    }

    /* Hide Chat Avatars & Icons Next to Messages */
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* Adjust Chat Message Padding after removing Avatars */
    [data-testid="stChatMessage"] {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        color: #E2E8F0;
    }

    /* Hide Prompt / Submit Button Icon */
    [data-testid="stChatInputSubmitButton"] svg {
        display: none !important;
    }

    /* Style Prompt Submit Button as clean text/border */
    [data-testid="stChatInputSubmitButton"] {
        background-color: #3B82F6 !important;
        border-radius: 6px !important;
        color: #FFFFFF !important;
    }
    
    [data-testid="stChatInputSubmitButton"]::after {
        content: "Send";
        font-size: 0.85rem;
        font-weight: 600;
        color: white;
    }

    /* Inputs Styling */
    .stTextInput input {
        background-color: #0F172A;
        color: #F8FAFC;
        border: 1px solid #334155;
        border-radius: 6px;
    }

    .stTextInput input:focus {
        border-color: #3B82F6;
        box-shadow: none;
    }

    /* Modern Metric Cards */
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #38BDF8;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Buttons */
    .stButton>button {
        background-color: #2563EB;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
        padding: 0.5rem 1rem;
    }

    .stButton>button:hover {
        background-color: #1D4ED8;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- Header ---
st.title("EDA STA Diagnostic Copilot")
st.caption("Automated Static Timing Analysis & Violation Root-Cause Assistant")
st.divider()

# --- Sidebar Configuration ---
with st.sidebar:
    st.subheader("System Configuration")

    st.markdown("**1. Ngrok Server Endpoint**")
    ngrok_url = st.text_input(
        "SERVER_URL",
        value=DEFAULT_NGROK_URL,
        label_visibility="collapsed",
        placeholder="https://your-ngrok-url.ngrok-free.dev",
    )

    st.markdown("**2. Groq API Key**")
    groq_key = st.text_input(
        "GROQ_KEY",
        value=DEFAULT_GROQ_KEY,
        type="password",
        label_visibility="collapsed",
    )

    st.markdown("**3. Upload Timing Report**")
    uploaded_file = st.file_uploader(
        "UPLOAD_FILE",
        type=["rpt", "txt", "log"],
        label_visibility="collapsed",
    )

    if st.button("Process & Index Report"):
        if not ngrok_url or not groq_key or not uploaded_file:
            st.error("Please provide server URL, API key, and report file.")
        else:
            with st.spinner("Indexing timing paths into vector store..."):
                try:
                    target_url = f"{ngrok_url.strip('/')}/upload"
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                    payload = {"groq_api_key": groq_key}

                    res = requests.post(target_url, files=files, data=payload)
                    if res.status_code == 200:
                        result = res.json()
                        if result.get("status") == "error":
                            st.error(f"Error: {result.get('message')}")
                        else:
                            st.session_state["processed"] = True
                            st.session_state["stats"] = result
                            st.session_state["ngrok_url"] = ngrok_url.strip("/")
                            st.success(f"Indexed {result['total_paths']} timing paths.")
                    else:
                        st.error(f"Server Error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

    # Display Metrics in Sidebar
    if st.session_state.get("processed"):
        stats = st.session_state["stats"]
        st.divider()
        st.subheader("Report Summary")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value">{stats["total_paths"]}</div><div class="metric-label">Total Paths</div></div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-value" style="color: #EF4444;">{stats["violations"]}</div><div class="metric-label">Violations</div></div>',
                unsafe_allow_html=True,
            )
            
        st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="metric-card"><div class="metric-value" style="color: #F59E0B;">{stats["wns"]:.3f} ns</div><div class="metric-label">Worst Negative Slack</div></div>',
            unsafe_allow_html=True,
        )

# --- Main Diagnostic Workspace ---
if not st.session_state.get("processed"):
    st.info("Upload and process an STA timing report from the sidebar to begin analysis.")
else:
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Render History without avatars
    for msg in st.session_state.chat_history:
        role_label = "**User**" if msg["role"] == "user" else "**Copilot**"
        with st.chat_message(msg["role"], avatar=None):
            st.markdown(f"{role_label}\n\n{msg['content']}")

    # Prompt Input
    if user_query := st.chat_input("Ask a diagnostic question (e.g., 'What are the main causes of slack violation?')..."):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        with st.chat_message("user", avatar=None):
            st.markdown(f"**User**\n\n{user_query}")

        with st.chat_message("assistant", avatar=None):
            with st.spinner("Analyzing timing paths..."):
                try:
                    query_url = f"{st.session_state['ngrok_url']}/query"
                    res = requests.post(query_url, json={"question": user_query})
                    if res.status_code == 200:
                        ans_data = res.json()
                        if ans_data.get("status") == "error":
                            answer = f"Error: {ans_data.get('message')}"
                        else:
                            answer = ans_data.get("answer", "No response generated.")
                        
                        st.markdown(f"**Copilot**\n\n{answer}")
                        st.session_state.chat_history.append({"role": "assistant", "content": answer})
                    else:
                        st.error(f"Server Error ({res.status_code}): {res.text}")
                except Exception as e:
                    st.error(f"Backend request failed: {e}")