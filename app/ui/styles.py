"""
Stable chat UI styles + wireframe header/sidebar.

Author: Vivek Kumar
"""

import base64
from functools import lru_cache
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WELCOME_THEME_IMAGE = PROJECT_ROOT / "Image" / "image_bc91fdd9.jpg"

DARK_BLUE = "#1565C0"
LIGHT_SKY_BLUE = "#D6F0FF"
BUTTON_TEXT = "#0D47A1"
HEADER_HEIGHT = "64px"
STAR_PATTERN = """
    radial-gradient(1.5px 1.5px at 25px 35px, #fff, transparent),
    radial-gradient(1px 1px at 80px 120px, rgba(255,255,255,0.9), transparent),
    radial-gradient(1.5px 1.5px at 140px 60px, #fff, transparent)
"""


@lru_cache(maxsize=1)
def _welcome_theme_background_data_url() -> str | None:
    """Load welcome theme image once as a CSS data URL."""
    if not WELCOME_THEME_IMAGE.is_file():
        return None

    encoded = base64.b64encode(WELCOME_THEME_IMAGE.read_bytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded}"


def _welcome_page_background_css() -> str:
    """Background for welcome page: theme image with overlay, or stars fallback."""
    image_url = _welcome_theme_background_data_url()
    if image_url:
        return f"""
                background-color: {DARK_BLUE} !important;
                background-image:
                    linear-gradient(rgba(13, 71, 161, 0.68), rgba(13, 71, 161, 0.82)),
                    url("{image_url}") !important;
                background-size: cover !important;
                background-position: center center !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed !important;
        """

    return f"""
                background-color: {DARK_BLUE} !important;
                background-image: {STAR_PATTERN} !important;
                background-size: 220px 220px !important;
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

            #MainMenu, footer, [data-testid="stToolbar"],
            [data-testid="stDecoration"], [data-testid="stStatusWidget"] {{
                visibility: hidden;
            }}

            header[data-testid="stHeader"] {{
                background: transparent !important;
                height: 0 !important;
                min-height: 0 !important;
            }}

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


def apply_welcome_layout_styles() -> None:
    """Hide sidebar and style the welcome landing page."""
    st.markdown(
        f"""
        <style>
            section[data-testid="stSidebar"],
            [data-testid="collapsedControl"] {{
                display: none !important;
            }}

            .stApp,
            [data-testid="stAppViewContainer"],
            [data-testid="stAppViewContainer"] > .main {{
                {_welcome_page_background_css()}
            }}

            [data-testid="stAppViewContainer"] > .main .block-container {{
                max-width: 820px !important;
                background-color: transparent !important;
                padding-bottom: 7rem !important;
            }}

            .app-disclaimer-footer {{
                background: rgba(13, 71, 161, 0.92) !important;
                border-top: 1px solid rgba(255, 255, 255, 0.25) !important;
                color: rgba(255, 255, 255, 0.88) !important;
            }}

            .welcome-page {{
                margin-top: 0.5rem;
            }}

            .welcome-hero {{
                text-align: center;
                margin-bottom: 1.25rem;
            }}

            .welcome-badge,
            .welcome-title,
            .welcome-subtitle {{
                text-align: center;
            }}

            .welcome-loading {{
                margin: 0.75rem 0 0.5rem 0;
                color: #FFFFFF !important;
                font-size: 0.92rem;
                font-weight: 600;
                text-align: center;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.45);
            }}

            .welcome-h {{
                margin: 1.1rem 0 0.45rem 0;
                color: #FFFFFF !important;
                font-size: 1.1rem;
                font-weight: 700;
                text-shadow: 0 1px 4px rgba(0, 0, 0, 0.45);
            }}

            .welcome-body {{
                margin: 0;
                color: #B3E5FC !important;
                line-height: 1.65;
                font-size: 0.98rem;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
            }}

            .welcome-bullet {{
                margin: 0.2rem 0 0 0;
                padding-left: 0.35rem;
            }}

            .welcome-h-builtby {{
                margin-bottom: 1.25rem !important;
            }}

            .welcome-name {{
                margin: 0.5rem 0 0 0;
                color: #FFFFFF !important;
                font-size: 1rem;
                font-weight: 700;
                text-shadow: 0 1px 4px rgba(0, 0, 0, 0.45);
            }}

            .welcome-note {{
                margin: 0.5rem 0 1rem 0;
                color: #81D4FA !important;
                font-size: 0.92rem;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
            }}

            .welcome-badge {{
                display: inline-block;
                margin: 0 0 1rem 0;
                padding: 0.35rem 0.75rem;
                background: rgba(255, 255, 255, 0.15);
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 999px;
                font-size: 0.82rem;
                font-weight: 600;
            }}

            .welcome-title {{
                margin: 0 0 0.35rem 0;
                color: #FFFFFF;
                font-size: 2rem;
                font-weight: 700;
                line-height: 1.2;
                text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
            }}

            .welcome-subtitle {{
                margin: 0;
                color: rgba(255, 255, 255, 0.92);
                font-size: 1.05rem;
            }}

            .welcome-section {{
                margin-bottom: 1.35rem;
            }}

            .welcome-section:last-child {{
                margin-bottom: 0;
            }}

            .welcome-section-title {{
                margin: 0 0 0.5rem 0;
                color: {DARK_BLUE};
                font-size: 1.05rem;
                font-weight: 700;
            }}

            .welcome-section p {{
                margin: 0;
                color: #37474F;
                line-height: 1.6;
                font-size: 0.98rem;
            }}

            .welcome-benefits {{
                margin: 0;
                padding-left: 1.25rem;
                color: #37474F;
                line-height: 1.7;
                font-size: 0.98rem;
            }}

            .welcome-author p {{
                margin: 0.15rem 0 0 0;
            }}

            .welcome-author-note {{
                margin-top: 0.5rem !important;
                color: #607D8B !important;
                font-size: 0.92rem !important;
            }}

            section.main [data-testid="stButton"],
            section[data-testid="stMain"] [data-testid="stButton"],
            section.main div.stButton,
            section[data-testid="stMain"] div.stButton {{
                margin-top: 0.75rem !important;
                margin-bottom: 2rem !important;
            }}

            section.main [data-testid="stButton"] button,
            section[data-testid="stMain"] [data-testid="stButton"] button,
            section.main div.stButton > button,
            section[data-testid="stMain"] div.stButton > button,
            section.main button[data-testid="stBaseButton-primary"],
            section[data-testid="stMain"] button[data-testid="stBaseButton-primary"] {{
                background-color: #FFFFFF !important;
                color: {BUTTON_TEXT} !important;
                -webkit-text-fill-color: {BUTTON_TEXT} !important;
                font-weight: 700 !important;
                font-size: 1rem !important;
                border: 2px solid #FFFFFF !important;
                border-radius: 10px !important;
                padding: 0.8rem 1rem !important;
                min-height: 3.1rem !important;
                width: 100% !important;
                box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35) !important;
                opacity: 1 !important;
                visibility: visible !important;
            }}

            section.main [data-testid="stButton"] button:disabled,
            section[data-testid="stMain"] [data-testid="stButton"] button:disabled {{
                background-color: #ECEFF1 !important;
                color: #546E7A !important;
                -webkit-text-fill-color: #546E7A !important;
                border-color: #CFD8DC !important;
            }}

            section.main [data-testid="stButton"] button:hover,
            section.main div.stButton > button:hover {{
                background-color: #E3F2FD !important;
            }}

            section.main [data-testid="stButton"] button p,
            section.main [data-testid="stButton"] button span,
            section.main [data-testid="stButton"] button div,
            section.main div.stButton > button p,
            section.main div.stButton > button span,
            section.main div.stButton > button div {{
                color: {BUTTON_TEXT} !important;
                -webkit-text-fill-color: {BUTTON_TEXT} !important;
            }}

            [data-testid="stAppViewContainer"] .main [data-testid="stCaptionContainer"] p {{
                color: #B3E5FC !important;
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
