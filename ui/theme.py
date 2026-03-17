import streamlit as st


def aplicar_tema() -> None:
    high_contrast = st.session_state.get("accessibility_high_contrast", False)
    large_text = st.session_state.get("accessibility_large_text", False)
    reduce_motion = st.session_state.get("accessibility_reduce_motion", True)

    body_font_size = "1.08rem" if large_text else "1rem"
    heading_size = "3rem" if large_text else "2.6rem"
    subheading_size = "2rem" if large_text else "1.8rem"
    button_text = "#f8fafc"
    button_bg = "linear-gradient(135deg, #1d4ed8 0%, #0f766e 100%)" if not high_contrast else "linear-gradient(135deg, #0b0f14 0%, #0b0f14 100%)"
    button_border = "#60a5fa" if not high_contrast else "#ffffff"
    page_bg = "linear-gradient(180deg, #06080d 0%, #0b1220 100%)" if high_contrast else "linear-gradient(180deg, #0b1220 0%, #111827 100%)"
    sidebar_bg = "linear-gradient(180deg, #08101c 0%, #0f172a 100%)"
    focus_color = "#ffffff" if high_contrast else "#7dd3fc"
    card_bg = "rgba(11, 18, 32, 0.96)" if high_contrast else "rgba(15, 23, 42, 0.86)"
    card_soft = "rgba(15, 23, 42, 0.92)" if high_contrast else "rgba(30, 41, 59, 0.72)"
    border_color = "rgba(255,255,255,0.38)" if high_contrast else "rgba(148, 163, 184, 0.18)"
    motion_css = "*" + " { animation: none !important; transition: none !important; scroll-behavior: auto !important; }" if reduce_motion else ""

    st.set_page_config(
        page_title="Arcade Cognitivo",
        page_icon="🎮",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        f"""
        <style>
        :root {{
            --bg: #0b1220;
            --surface: {card_bg};
            --surface-strong: rgba(15, 23, 42, 0.98);
            --surface-soft: {card_soft};
            --ink: #f8fafc;
            --muted: #cbd5e1;
            --accent: #22c55e;
            --accent-2: #06b6d4;
            --accent-3: #f59e0b;
            --danger: #fb7185;
            --border: {border_color};
            --focus: {focus_color};
            --shadow: 0 18px 40px rgba(2, 6, 23, 0.28);
        }}

        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(34, 197, 94, 0.10), transparent 20%),
                radial-gradient(circle at top right, rgba(6, 182, 212, 0.12), transparent 22%),
                {page_bg};
            color: var(--ink);
            font-family: "Segoe UI", "Inter", sans-serif;
            font-size: {body_font_size};
        }}

        .main .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }}

        h1, h2, h3 {{
            color: var(--ink);
            letter-spacing: -0.02em;
            line-height: 1.1;
            transform: none;
        }}

        h1 {{ font-size: {heading_size}; }}
        h2 {{ font-size: {subheading_size}; }}

        p, li, label, .stMarkdown, .stCaption, .stTextInput, .stNumberInput, .stRadio, .stSelectbox {{
            color: var(--ink);
            line-height: 1.55;
        }}

        [data-testid="stSidebar"] {{
            background: {sidebar_bg};
            border-right: 1px solid var(--border);
        }}

        [data-testid="stSidebar"] * {{
            color: var(--ink);
        }}

        [data-testid="stMetricValue"] {{
            color: var(--ink);
        }}

        div[data-testid="stVerticalBlock"] div[data-testid="stContainer"] {{
            border-radius: 18px;
        }}

        div[data-testid="stContainer"] {{
            background: transparent;
        }}

        [data-testid="stMetric"],
        div[data-testid="stForm"],
        div[data-testid="stAlert"],
        div[data-testid="stExpander"] {{
            background: var(--surface);
            border: 1px solid var(--border);
            backdrop-filter: blur(12px);
            box-shadow: var(--shadow);
            border-radius: 20px;
        }}

        .stButton > button {{
            min-height: 2.9rem;
            border-radius: 16px;
            border: 1px solid {button_border};
            background: {button_bg};
            color: {button_text};
            font-weight: 700;
            font-size: 1rem;
            letter-spacing: 0.02em;
            transition: box-shadow 140ms ease, filter 140ms ease, border-color 140ms ease;
        }}

        .stButton > button p,
        .stButton > button span,
        .stButton > button div {{
            color: {button_text} !important;
        }}

        .stButton > button:hover {{
            border-color: var(--focus);
            filter: brightness(1.02);
            transform: none;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.22);
        }}

        .stButton > button:active {{
            transform: none;
            filter: brightness(0.99);
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.18);
        }}

        .stButton > button:disabled {{
            opacity: 0.62;
            color: {button_text} !important;
            background: linear-gradient(135deg, rgba(100, 116, 139, 0.95) 0%, rgba(71, 85, 105, 0.95) 100%);
        }}

        .stTextInput input, .stNumberInput input, textarea {{
            border-radius: 14px;
            background: var(--surface-strong);
            border: 1px solid var(--border);
            color: var(--ink);
            font-size: 1rem;
            min-height: 2.8rem;
        }}

        .stTextInput input::placeholder,
        textarea::placeholder {{
            color: var(--muted);
        }}

        div[data-baseweb="select"] > div,
        .stRadio > div,
        .stSegmentedControl {{
            background: var(--surface-soft);
            border-radius: 14px;
            border: 1px solid var(--border);
            padding: 0.25rem;
        }}

        div[data-baseweb="select"] {{
            line-height: 1.2 !important;
        }}

        div[data-baseweb="select"] > div {{
            min-height: 2.9rem;
            align-items: center !important;
            padding-top: 0.18rem;
            padding-bottom: 0.18rem;
        }}

        div[data-baseweb="select"] input,
        div[data-baseweb="select"] div[role="combobox"],
        div[data-baseweb="select"] [aria-selected="true"],
        div[data-baseweb="select"] span {{
            line-height: 1.2 !important;
            min-height: auto !important;
            display: flex;
            align-items: center;
        }}

        div[data-baseweb="popover"] ul,
        div[role="listbox"] {{
            line-height: 1.35 !important;
        }}

        div[role="option"] {{
            min-height: 2.5rem;
            display: flex;
            align-items: center;
            padding-top: 0.35rem !important;
            padding-bottom: 0.35rem !important;
        }}

        .stCheckbox label, .stRadio label {{
            color: var(--ink) !important;
        }}

        .stMultiSelect [data-baseweb="tag"] {{
            background: rgba(6, 182, 212, 0.18);
            color: var(--ink);
        }}

        .stCodeBlock, pre, code {{
            font-family: "JetBrains Mono", "Fira Code", monospace !important;
        }}

        .page-hero,
        .game-hero {{
            position: relative;
            overflow: hidden;
            padding: 1.4rem 1.45rem;
            border-radius: 24px;
            border: 1px solid var(--border);
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 41, 59, 0.92) 100%);
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
        }}

        .page-hero::before,
        .game-hero::before {{
            content: "";
            position: absolute;
            inset: 0;
            background: linear-gradient(120deg, transparent 0%, rgba(6, 182, 212, 0.10) 36%, transparent 72%);
            pointer-events: none;
        }}

        .page-hero h1,
        .game-hero h2 {{
            margin: 0;
            color: var(--ink);
        }}

        .page-hero p,
        .game-hero p {{
            margin: 0.45rem 0 0;
            color: var(--muted);
            max-width: 62rem;
        }}

        .page-hero-chip,
        .game-hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            margin-bottom: 0.7rem;
            padding: 0.32rem 0.72rem;
            border-radius: 999px;
            border: 1px solid rgba(6, 182, 212, 0.24);
            background: rgba(6, 182, 212, 0.12);
            color: #cffafe;
            font-size: 0.88rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
        }}

        .metric-shell {{
            display: flex;
            flex-direction: column;
            gap: 0.35rem;
            min-height: 100%;
            padding: 1rem 1.05rem;
            border-radius: 20px;
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(15, 23, 42, 0.92) 100%);
            box-shadow: var(--shadow);
        }}

        .metric-label {{
            color: var(--muted);
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }}

        .metric-value {{
            color: var(--ink);
            font-size: 1.5rem;
            line-height: 1.1;
        }}

        .metric-help {{
            color: #9fbbd9;
            font-size: 0.92rem;
        }}

        .game-card-shell {{
            min-height: 8.4rem;
        }}

        .game-card-tag {{
            display: inline-flex;
            margin-bottom: 0.8rem;
            padding: 0.24rem 0.62rem;
            border-radius: 999px;
            background: rgba(34, 197, 94, 0.10);
            border: 1px solid rgba(34, 197, 94, 0.18);
            color: #dcfce7;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }}

        .game-card-top {{
            display: grid;
            grid-template-columns: 56px 1fr;
            gap: 0.9rem;
            align-items: start;
        }}

        .game-card-emoji {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 56px;
            height: 56px;
            border-radius: 18px;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.16) 0%, rgba(34, 197, 94, 0.12) 100%);
            border: 1px solid rgba(6, 182, 212, 0.22);
            font-size: 1.7rem;
        }}

        .game-card-title {{
            color: var(--ink);
            font-size: 1.25rem;
            font-weight: 700;
        }}

        .game-card-copy {{
            color: var(--muted);
            margin-top: 0.32rem;
        }}

        .spotlight-panel,
        .side-panel-shell,
        .championship-row {{
            border: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(15, 23, 42, 0.92) 100%);
            box-shadow: var(--shadow);
        }}

        .spotlight-panel {{
            padding: 1.15rem 1.2rem;
            border-radius: 24px;
            margin-bottom: 1rem;
        }}

        .spotlight-panel h3 {{
            margin: 0.25rem 0 0;
        }}

        .spotlight-panel p {{
            color: var(--muted);
            margin: 0.45rem 0 0.8rem;
        }}

        .spotlight-kicker {{
            color: #e2e8f0;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.78rem;
            font-weight: 700;
        }}

        .spotlight-chip-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}

        .spotlight-chip {{
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            background: rgba(51, 65, 85, 0.52);
            border: 1px solid var(--border);
            color: #e2e8f0;
            font-size: 0.84rem;
        }}

        .side-panel-shell {{
            position: sticky;
            top: 1rem;
            padding: 1rem 1.05rem;
            border-radius: 22px;
        }}

        .side-panel-title {{
            color: var(--ink);
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
        }}

        .side-panel-row {{
            display: flex;
            justify-content: space-between;
            gap: 0.75rem;
            padding: 0.62rem 0;
            border-top: 1px solid var(--border);
            color: var(--muted);
        }}

        .side-panel-row:first-of-type {{
            border-top: 0;
            padding-top: 0;
        }}

        .side-panel-row strong {{
            color: var(--ink);
            text-align: right;
        }}

        .side-panel-note {{
            margin-top: 0.9rem;
            padding: 0.75rem 0.85rem;
            border-radius: 16px;
            background: rgba(51, 65, 85, 0.52);
            color: #e2e8f0;
            font-size: 0.92rem;
        }}

        .championship-row {{
            display: grid;
            grid-template-columns: 72px 1fr auto;
            align-items: center;
            gap: 1rem;
            padding: 0.95rem 1rem;
            border-radius: 20px;
            margin-bottom: 0.75rem;
        }}

        .championship-position {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            min-height: 52px;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.16) 0%, rgba(245, 158, 11, 0.16) 100%);
            border: 1px solid var(--border);
            font-weight: 700;
        }}

        .championship-player {{
            display: flex;
            flex-direction: column;
            gap: 0.24rem;
        }}

        .championship-player strong {{
            color: var(--ink);
            font-size: 1rem;
        }}

        .championship-game {{
            color: var(--muted);
            font-size: 0.88rem;
        }}

        .championship-score {{
            color: #d1fae5;
            font-size: 1.08rem;
            font-weight: 700;
        }}

        .home-grid-note {{
            color: var(--muted);
            margin-bottom: 0.8rem;
        }}

        .stAlert {{
            border-radius: 16px;
        }}

        *:focus-visible {{
            outline: 3px solid {focus_color} !important;
            outline-offset: 2px !important;
            box-shadow: none !important;
        }}

        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation: none !important;
                transition: none !important;
                scroll-behavior: auto !important;
            }}
        }}

        {motion_css}
        </style>
        """,
        unsafe_allow_html=True,
    )
