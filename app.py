from translator import translate_text
from speech import speech_to_text, text_to_speech
from language_detector import detect_language
from database import save_translation, get_history, clear_history
import streamlit as st

st.set_page_config(
    page_title="LinguaAI Translator",
    page_icon="🌐",
    layout="wide",
)

if "source_text" not in st.session_state:
    st.session_state.source_text = ""
if "translation_output" not in st.session_state:
    st.session_state.translation_output = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""

LANGUAGE_OPTIONS = [
    "English",
    "Hindi",
    "Telugu",
    "Tamil",
    "French",
    "German",
    "Spanish"
]

language_codes = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "French": "fr",
    "German": "de",
    "Spanish": "es"
}

speech_language_codes = {
    "English": "en-US",
    "Hindi": "hi-IN",
    "Telugu": "te-IN",
    "Tamil": "ta-IN",
    "French": "fr-FR",
    "German": "de-DE",
    "Spanish": "es-ES"
}

st.markdown(
    """
    <style>
    :root {
        --bg: #f7f9ff;
        --panel: rgba(255, 255, 255, 0.76);
        --line: rgba(92, 113, 255, 0.16);
        --text: #132238;
        --muted: #5c6e8a;
        --blue: #4f7cff;
        --purple: #8a6df5;
        --soft: #e6efff;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top left, rgba(79, 124, 255, 0.16), transparent 24%),
            radial-gradient(circle at bottom right, rgba(138, 109, 245, 0.14), transparent 28%),
            var(--bg);
    }

    [data-testid="stHeader"] {
        background: transparent;
        box-shadow: none;
    }

    .block-container {
        padding-top: 1.3rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero-shell {
        display: grid;
        grid-template-columns: 1.5fr 0.8fr;
        gap: 1.2rem;
        padding: 1.4rem;
        border-radius: 30px;
        background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(240,245,255,0.86));
        border: 1px solid var(--line);
        box-shadow: 0 20px 60px rgba(75, 101, 183, 0.12);
        margin-bottom: 1.2rem;
        overflow: hidden;
    }

    .hero-copy h1 {
        font-size: 2.4rem;
        font-weight: 700;
        line-height: 1.1;
        letter-spacing: -0.03em;
        color: var(--text);
        margin: 0.2rem 0 0.45rem;
    }

    .hero-copy p {
        font-size: 1.04rem;
        color: var(--muted);
        margin-bottom: 0.8rem;
        max-width: 720px;
    }

    .eyebrow {
        display: inline-flex;
        padding: 0.4rem 0.7rem;
        border-radius: 999px;
        background: rgba(79, 124, 255, 0.1);
        color: var(--blue);
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.14em;
        text-transform: uppercase;
    }

    .pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
        margin-top: 0.6rem;
    }

    .pill {
        padding: 0.43rem 0.75rem;
        border-radius: 999px;
        background: rgba(138, 109, 245, 0.09);
        color: #5c51aa;
        font-size: 0.8rem;
        border: 1px solid rgba(138, 109, 245, 0.16);
    }

    .hero-stats {
        display: grid;
        gap: 0.7rem;
        align-content: center;
    }

    .stat-card {
        padding: 0.9rem 1rem;
        border-radius: 20px;
        background: var(--panel);
        border: 1px solid var(--line);
        box-shadow: 0 10px 24px rgba(75, 101, 183, 0.09);
    }

    .stat-card strong {
        color: var(--text);
        display: block;
        font-size: 1.15rem;
        margin-bottom: 0.2rem;
    }

    .stat-card span {
        color: var(--muted);
        font-size: 0.9rem;
    }

    .workspace-panel {
        padding: 1.2rem;
        border-radius: 30px;
        background: rgba(255, 255, 255, 0.72);
        border: 1px solid var(--line);
        box-shadow: 0 18px 50px rgba(75, 101, 183, 0.11);
        backdrop-filter: blur(18px);
        margin-bottom: 1rem;
    }

    .panel-title {
        font-size: 1.08rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.2rem;
    }

    .panel-subtitle {
        color: var(--muted);
        font-size: 0.95rem;
        margin-bottom: 0.9rem;
    }

    .lang-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        align-items: center;
        margin-bottom: 0.8rem;
    }

    .lang-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.7rem 0.95rem;
        border-radius: 999px;
        background: linear-gradient(90deg, rgba(79, 124, 255, 0.12), rgba(138, 109, 245, 0.1));
        color: var(--text);
        font-weight: 600;
        border: 1px solid rgba(79, 124, 255, 0.14);
    }

    .swap-btn {
        border: 0;
        border-radius: 999px;
        padding: 0.7rem 0.9rem;
        color: white;
        background: linear-gradient(90deg, var(--blue), var(--purple));
        box-shadow: 0 10px 24px rgba(79, 124, 255, 0.18);
        transition: transform 180ms ease, box-shadow 180ms ease;
    }

    .swap-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 28px rgba(79, 124, 255, 0.24);
    }

    .editor-card {
        padding: 1rem;
        border-radius: 24px;
        background: linear-gradient(180deg, #ffffff, #f8fbff);
        border: 1px solid rgba(79, 124, 255, 0.14);
        min-height: 250px;
    }

    .editor-label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        color: var(--text);
        font-weight: 600;
    }

    .editor-label span {
        color: var(--muted);
        font-size: 0.85rem;
        font-weight: 500;
    }

    .feature-card {
        padding: 1rem;
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(255,255,255,0.92), rgba(242,247,255,0.88));
        border: 1px solid var(--line);
        box-shadow: 0 10px 28px rgba(75, 101, 183, 0.07);
        min-height: 130px;
    }

    .feature-card h4 {
        margin: 0.35rem 0 0.25rem;
        color: var(--text);
        font-size: 0.98rem;
    }

    .feature-card p {
        color: var(--muted);
        font-size: 0.9rem;
        margin: 0;
    }

    .icon-badge {
        width: 38px;
        height: 38px;
        display: inline-grid;
        place-items: center;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(79, 124, 255, 0.16), rgba(138, 109, 245, 0.14));
        color: var(--blue);
        font-size: 1rem;
    }

    .history-card {
        padding: 1rem;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(241,246,255,0.88));
        border: 1px solid var(--line);
        margin-top: 0.7rem;
    }

    .history-card h4 {
        margin: 0 0 0.5rem;
        color: var(--text);
    }

    .history-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem 0;
        border-bottom: 1px solid rgba(79, 124, 255, 0.1);
        color: var(--muted);
    }

    .history-item:last-child {
        border-bottom: none;
    }

    .stTextArea textarea {
    background: rgba(255,255,255,0.92) !important;
    color: #132238 !important;
    -webkit-text-fill-color: #132238 !important;

    border: 1px solid rgba(79,124,255,0.18) !important;
    border-radius: 18px !important;

    box-shadow: 0 8px 24px rgba(79,124,255,0.08) !important;
    outline: none !important;
    }

    .stTextArea textarea:focus {
    border: 1px solid #4f7cff !important;
    box-shadow: 0 0 0 3px rgba(79,124,255,0.15) !important;
    }

    .stTextInput input {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(79,124,255,0.18) !important;
    border-radius: 18px !important;
    color: #132238 !important;
    -webkit-text-fill-color: #132238 !important;
    }

    /* Streamlit 1.60.0 Selectbox Fix */
    div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(79,124,255,0.16) !important;
    border-radius: 16px !important;
    color: #132238 !important;
    }

    div[data-baseweb="select"] span {
    color: #132238 !important;
    }

    div[data-baseweb="select"] input {
    color: #132238 !important;
    -webkit-text-fill-color: #132238 !important;
    }

    /* Make Source Language and Target Language labels clearly visible */
    .stSelectbox label {
    color: #132238 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    margin-bottom: 6px !important;
   }

    .stButton > button {
        width: 100%;
        border-radius: 999px;
        border: none;
        padding: 0.8rem 1.1rem;
        color: white;
        font-weight: 700;
        background: linear-gradient(90deg, var(--blue), var(--purple));
        box-shadow: 0 12px 24px rgba(79, 124, 255, 0.18);
        transition: transform 180ms ease, box-shadow 180ms ease;
    }

    /* Translation spinner visibility */
div[data-testid="stSpinner"] {
    background: rgba(255, 255, 255, 0.95) !important;
    border: 1px solid rgba(79, 124, 255, 0.18) !important;
    border-radius: 14px !important;
    padding: 0.7rem 1rem !important;
}

div[data-testid="stSpinner"] p {
    color: #132238 !important;
    font-weight: 700 !important;
}

/* Download Translation button */
.stDownloadButton > button {
    width: 100% !important;
    border-radius: 999px !important;
    border: none !important;
    padding: 0.8rem 1.1rem !important;
    color: white !important;
    background: linear-gradient(90deg, var(--blue), var(--purple)) !important;
    font-weight: 700 !important;
    box-shadow: 0 12px 24px rgba(79, 124, 255, 0.18) !important;
}

.stDownloadButton > button:hover,
.stDownloadButton > button:focus,
.stDownloadButton > button:active {
    color: white !important;
    background: linear-gradient(90deg, var(--blue), var(--purple)) !important;
    border: none !important;
}

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 14px 28px rgba(79, 124, 255, 0.24);
        border: none;
    }

    @media (max-width: 1000px) {
        .hero-shell { grid-template-columns: 1fr; }
        .feature-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }

    @media (max-width: 680px) {
        .feature-grid { grid-template-columns: 1fr; }
    }

    /* Fix selected value inside Streamlit selectbox */
    div[data-baseweb="select"] div {
    color: #132238 !important;
}

    div[data-baseweb="select"] svg {
    color: #132238 !important;
    fill: #132238 !important;
}
   
    /* Warning message visibility fix */
div[data-testid="stAlert"] {
    background-color: #FFF3CD !important;
    border: 1px solid #FFCA2C !important;
    border-radius: 16px !important;
}

div[data-testid="stAlert"] p {
    color: #664D03 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-shell">
        <div class="hero-copy">
            <div class="eyebrow">Global AI Translation</div>
            <h1>Break Language Barriers with AI</h1>
            <p>Translate text instantly across multiple languages with intelligent AI technology designed for modern global teams.</p>
            <div class="pill-row">
                <span class="pill">Secure by design</span>
                <span class="pill">Instant outcomes</span>
                <span class="pill">Trusted worldwide</span>
            </div>
        </div>
        <div class="hero-stats">
            <div class="stat-card">
                <strong>98.4% clarity</strong>
                <span>Optimized for natural, fluid results</span>
            </div>
            <div class="stat-card">
                <strong>24/7 intelligence</strong>
                <span>Reliable for fast-moving product teams</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="workspace-panel">
        <div class="panel-title">Live Translation Workspace</div>
        <div class="panel-subtitle">A refined experience for everyday multilingual communication.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

source_col, target_col = st.columns([1, 1])

with source_col:

    source_language = st.selectbox(
        "Source Language",
        LANGUAGE_OPTIONS,
        index=0,
        key="source_language"
    )

    if st.button("🔍 Detect Language"):

        detected = detect_language(
            st.session_state.source_text
        )

        st.info(
            f"Detected language code: {detected}"
        )

with target_col:
    target_language = st.selectbox(
        "Target Language",
        LANGUAGE_OPTIONS,
        index=2,
        key="target_language"
    )

# Clear previous translation when language selection changes
if (
    "prev_source_language" not in st.session_state or
    "prev_target_language" not in st.session_state
):
    st.session_state.prev_source_language = source_language
    st.session_state.prev_target_language = target_language
else:
    if (
        source_language != st.session_state.prev_source_language or
        target_language != st.session_state.prev_target_language
    ):
        st.session_state.translation_output = ""
        st.session_state.prev_source_language = source_language
        st.session_state.prev_target_language = target_language

st.markdown('<div class="lang-row">', unsafe_allow_html=True)
st.markdown(f'<span class="lang-pill">{source_language} → {target_language}</span>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1], gap="large")

with left_col:

    if st.session_state.voice_text:
        st.session_state.source_text = st.session_state.voice_text
        st.session_state.voice_text = ""

    st.markdown(
        """
        <div class="editor-card">
            <div class="editor-label">Source text <span>Context-aware input</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.text_area("", height=160, key="source_text")

    if st.button("🎤 Speak", use_container_width=True):

        voice_text = speech_to_text(
            speech_language_codes[source_language]
        )

        if (
            not voice_text.startswith("Error")
            and not voice_text.startswith("Could")
        ):
            st.session_state.voice_text = voice_text
            st.rerun()

        else:
            st.error(voice_text)
        
with right_col:
    st.markdown(
        """
        <div class="editor-card">
            <div class="editor-label">Translation output <span>Elegant AI response</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.text_area(
    "",
    value=st.session_state.translation_output,
    height=160,
    disabled=True,
    )

    if st.session_state.translation_output:

        if st.button("🔊 Listen Translation", use_container_width=True):

            text_to_speech(
                st.session_state.translation_output,
                language_codes[target_language]
            )
 
    if st.session_state.translation_output:

        st.download_button(
            label="⬇️ Download Translation",
            data=st.session_state.translation_output,
            file_name="translation.txt",
            mime="text/plain"
        )

st.markdown("<div style='margin: 0.8rem 0;'></div>", unsafe_allow_html=True)

action_col, _, _ = st.columns([1, 1, 1])

with action_col:
    if st.button("Translate Now", use_container_width=True):

        if not st.session_state.source_text.strip():
            st.warning("⚠️ Please enter some text to translate.")

        else:
            try:
                with st.spinner("🤖 AI is translating..."):

                    translated = translate_text(
                        st.session_state.source_text,
                        source_language,
                        target_language
                    )

                st.session_state.translation_output = translated
                st.success("✅ Translation completed successfully!")

                if st.session_state.source_text.strip():
                    save_translation(
                        st.session_state.source_text,
                        translated,
                        f"{source_language} → {target_language}"
                    )
                    st.session_state.history = st.session_state.history[:10]

                st.rerun()

            except Exception as e:
                st.error(f"❌ Translation failed: {e}")

features = [
    ("✨", "AI Powered Translation", "Natural, nuanced wording for modern global communication."),
    ("🌍", "Multiple Language Support", "Expand into new markets with confidence and speed."),
    ("🎙️", "Voice Translation", "Handcrafted workflows for spoken conversations and live content."),
    ("🕘", "Translation History", "Keep your recent exchanges organized and easy to revisit."),
    ("🔍","Auto Language Detection","Automatically identifies input language."),
]

feature_cols = st.columns(5)
for col, (icon, title, desc) in zip(feature_cols, features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="icon-badge">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown(
    """
    <div class="history-card">
        <h4>Recent translation activity</h4>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)

if st.button("🗑️ Clear History"):

    clear_history()

    st.success(
        "History cleared successfully"
    )

    st.rerun()

history_data = get_history()

for item in history_data:
    st.markdown(
    f"""
    <div class="history-item">
        <div>
            <strong>{item.source_text}</strong><br>
            <small>{item.translated_text}</small>
        </div>
        <span>{item.language_pair}</span>
    </div>
    """,
    unsafe_allow_html=True,
)