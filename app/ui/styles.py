"""
Stable chat UI styles + wireframe header/sidebar.

Author: Vivek Kumar
"""

import streamlit as st

DARK_BLUE = "#1565C0"
LIGHT_SKY_BLUE = "#D6F0FF"
BUTTON_TEXT = "#0D47A1"
HEADER_HEIGHT = "64px"
STAR_PATTERN = """
    radial-gradient(1.5px 1.5px at 25px 35px, #fff, transparent),
    radial-gradient(1px 1px at 80px 120px, rgba(255,255,255,0.9), transparent),
    radial-gradient(1.5px 1.5px at 140px 60px, #fff, transparent)
"""


def apply_wireframe_styles() -> None:
    st.markdown(
        f"""
        <style>
            header[data-testid="stHeader"] {{
                background: transparent !important;
            }}

            .wireframe-header-full {{
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                width: 100%;
                height: {HEADER_HEIGHT};
                z-index: 1000;
                background-color: {DARK_BLUE};
                background-image: {STAR_PATTERN};
                background-size: 220px 220px;
                color: #FFFFFF;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.15rem;
                font-weight: 600;
            }}

            .header-spacer {{
                height: {HEADER_HEIGHT};
            }}

            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewContainer"] > .main {{
                background-color: {LIGHT_SKY_BLUE} !important;
            }}

            [data-testid="stAppViewContainer"] > .main .block-container {{
                padding-top: 0.75rem !important;
                padding-bottom: 6rem !important;
                max-width: 900px !important;
                margin: 0 auto !important;
                background-color: {LIGHT_SKY_BLUE} !important;
            }}

            section[data-testid="stSidebar"] {{
                background-color: {DARK_BLUE} !important;
                background-image: {STAR_PATTERN} !important;
                background-size: 180px 180px !important;
                padding-top: {HEADER_HEIGHT} !important;
            }}

            section[data-testid="stSidebar"] > div {{
                background-color: transparent !important;
                height: calc(100vh - {HEADER_HEIGHT}) !important;
                overflow-y: auto !important;
            }}

            section[data-testid="stSidebar"] h2,
            section[data-testid="stSidebar"] label,
            section[data-testid="stSidebar"] p {{
                color: #FFFFFF !important;
            }}

            section[data-testid="stSidebar"] .knowledge-scope-list {{
                margin: 0.25rem 0 0 0;
                padding-left: 1.25rem;
                color: #FFFFFF !important;
                font-weight: 600;
                font-size: 0.95rem;
                line-height: 1.7;
            }}

            section[data-testid="stSidebar"] .knowledge-scope-list li {{
                color: #FFFFFF !important;
                margin-bottom: 0.15rem;
            }}

            section[data-testid="stSidebar"] .knowledge-scope-empty {{
                color: rgba(255, 255, 255, 0.9) !important;
                font-size: 0.9rem;
                margin: 0;
            }}

            section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {{
                color: rgba(255, 255, 255, 0.85) !important;
                font-size: 0.82rem !important;
            }}

            section[data-testid="stSidebar"] hr {{
                border-color: rgba(255,255,255,0.35) !important;
            }}

            section[data-testid="stSidebar"] div.stButton > button {{
                background-color: #FFFFFF !important;
                color: {BUTTON_TEXT} !important;
                font-weight: 700 !important;
                width: 100% !important;
                border: none !important;
                border-radius: 8px !important;
                margin-top: 0.5rem !important;
            }}

            section[data-testid="stSidebar"] div.stButton > button p,
            section[data-testid="stSidebar"] div.stButton > button span,
            section[data-testid="stSidebar"] div.stButton > button div {{
                color: {BUTTON_TEXT} !important;
            }}

            .stChatMessage {{
                background-color: #FFFFFF !important;
                border: 1px solid #BFDFFF !important;
                border-radius: 10px !important;
                padding: 0.75rem 1rem !important;
                margin-bottom: 0.75rem !important;
            }}

            .stChatMessage p,
            .stChatMessage span,
            .stChatMessage div[data-testid="stMarkdownContainer"] {{
                color: #1F2937 !important;
            }}

            [data-testid="stBottomBlockContainer"] {{
                background-color: {LIGHT_SKY_BLUE} !important;
                z-index: 1001 !important;
            }}

            [data-testid="stChatInput"] > div {{
                background: #FFFFFF !important;
                border: 1px solid #90CAF9 !important;
                border-radius: 10px !important;
            }}

            [data-testid="stChatInput"] textarea {{
                color: #1F2937 !important;
            }}

            .thinking-dots span {{
                display: inline-block;
                width: 7px;
                height: 7px;
                margin-right: 5px;
                background: #64748B;
                border-radius: 50%;
                animation: typing-dot 1.4s infinite ease-in-out both;
            }}

            .thinking-dots span:nth-child(1) {{ animation-delay: -0.32s; }}
            .thinking-dots span:nth-child(2) {{ animation-delay: -0.16s; }}

            .source-citations {{
                margin-top: 0.65rem;
                padding-top: 0.55rem;
                border-top: 1px solid #E2E8F0;
                font-size: 0.85rem;
                color: #475569 !important;
            }}

            .source-citations ul {{
                margin: 0.35rem 0 0 0;
                padding-left: 1.2rem;
            }}

            .source-citations li {{
                margin-bottom: 0.15rem;
            }}

            @keyframes typing-dot {{
                0%, 80%, 100% {{ transform: scale(0.6); opacity: 0.5; }}
                40% {{ transform: scale(1); opacity: 1; }}
            }}

            #MainMenu, footer {{ visibility: hidden; }}

            .app-disclaimer-footer {{
                position: fixed;
                bottom: 0;
                right: 0;
                left: 0;
                z-index: 999;
                background: rgba(255, 255, 255, 0.92);
                border-top: 1px solid #90CAF9;
                padding: 0.35rem 1rem;
                font-size: 0.72rem;
                color: #546E7A;
                text-align: center;
                line-height: 1.35;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header_banner() -> None:
    st.markdown(
        '<div class="wireframe-header-full">'
        "Oeeggis Corporation - Enterprise Knowledge Assistant"
        "</div>"
        '<div class="header-spacer"></div>',
        unsafe_allow_html=True,
    )


def render_footer_disclaimer(disclaimer_text: str) -> None:
    st.markdown(
        f'<div class="app-disclaimer-footer">{disclaimer_text}</div>',
        unsafe_allow_html=True,
    )
