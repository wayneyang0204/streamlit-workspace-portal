"""Unified launcher for the owner's Streamlit applications."""

from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

from portal_registry import load_portal_apps


RESOURCE_DIR = Path(__file__).resolve().parent
OFFICIAL_PROFILE_URL = "https://share.streamlit.io/user/wayneyang0204"


def _apply_portal_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --portal-ink: #17313a;
            --portal-muted: #60747b;
            --portal-teal: #007d8c;
            --portal-teal-dark: #075c67;
            --portal-line: rgba(0, 125, 140, 0.16);
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 8% 5%, rgba(0, 125, 140, 0.11), transparent 30rem),
                radial-gradient(circle at 94% 95%, rgba(31, 119, 180, 0.08), transparent 34rem),
                #f8fbfc;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1080px;
            padding-top: 2.5rem;
            padding-bottom: 2rem;
        }

        header[data-testid="stHeader"] {
            display: none;
        }

        [data-testid="stLogoSpacer"],
        [data-testid="stSidebar"] {
            display: none;
        }

        [data-testid="stImage"] {
            display: flex;
            justify-content: center;
            margin: 0 auto 0.8rem;
        }

        [data-testid="stImage"] img {
            width: min(310px, 76vw);
            height: auto;
        }

        .portal-wordmark {
            margin: 0 auto 1rem;
            color: var(--portal-teal);
            font-size: clamp(3rem, 8vw, 4.9rem);
            font-style: italic;
            font-weight: 850;
            letter-spacing: -0.08em;
            line-height: 0.86;
            text-align: center;
        }

        .portal-wordmark span {
            display: block;
            margin-top: 0.75rem;
            color: #31464e;
            font-size: 0.72rem;
            font-style: normal;
            font-weight: 800;
            letter-spacing: 0.42em;
        }

        .portal-kicker {
            margin: 0 0 0.45rem;
            color: var(--portal-teal);
            font-size: 0.76rem;
            font-weight: 800;
            letter-spacing: 0.18em;
            text-align: center;
        }

        .portal-title {
            margin: 0;
            color: var(--portal-ink);
            font-size: clamp(2rem, 5vw, 3.35rem);
            font-weight: 800;
            letter-spacing: -0.045em;
            line-height: 1.08;
            text-align: center;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            min-height: 250px;
            border: 1px solid var(--portal-line);
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.93);
            box-shadow: 0 16px 46px rgba(28, 65, 76, 0.08);
            transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-3px);
            border-color: rgba(0, 125, 140, 0.38);
            box-shadow: 0 21px 54px rgba(28, 65, 76, 0.13);
        }

        .portal-card-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 3.3rem;
            height: 3.3rem;
            margin-bottom: 0.75rem;
            border-radius: 16px;
            background: linear-gradient(145deg, rgba(0, 125, 140, 0.14), rgba(0, 125, 140, 0.05));
            font-size: 1.65rem;
        }

        .portal-card-eyebrow {
            margin-bottom: 0.28rem;
            color: var(--portal-teal);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.14em;
        }

        .portal-card-title {
            min-height: 3.05rem;
            margin: 0;
            color: var(--portal-ink);
            font-size: 1.38rem;
            font-weight: 780;
            line-height: 1.28;
        }

        [data-testid="stLinkButton"] a {
            border-radius: 12px;
            font-weight: 750;
        }

        [data-testid="stLinkButton"] a[kind="primary"] {
            border-color: var(--portal-teal);
            background: var(--portal-teal);
        }

        [data-testid="stLinkButton"] a[kind="primary"]:hover {
            border-color: var(--portal-teal-dark);
            background: var(--portal-teal-dark);
        }

        @media (max-width: 720px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1.35rem 1rem 1.5rem;
            }

            [data-testid="stHorizontalBlock"] {
                flex-direction: column;
            }

            [data-testid="column"] {
                width: 100% !important;
                flex: 1 1 100% !important;
            }

            [data-testid="stVerticalBlockBorderWrapper"] {
                min-height: auto;
            }

            .portal-card-title {
                min-height: auto;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _render_app_card(app: dict[str, str]) -> None:
    icon = escape(app.get("icon", "🚀"))
    eyebrow = escape(app.get("eyebrow", "STREAMLIT APP"))
    name = escape(app["name"])
    with st.container(border=True):
        st.markdown(
            (
                f'<div class="portal-card-icon" aria-hidden="true">{icon}</div>'
                f'<div class="portal-card-eyebrow">{eyebrow}</div>'
                f'<div class="portal-card-title">{name}</div>'
            ),
            unsafe_allow_html=True,
        )
        st.link_button(
            app["button"],
            app["url"],
            icon=":material/arrow_outward:",
            type="primary",
            width="stretch",
        )
        if app.get("admin_url"):
            st.link_button(
                "文件系統管理員入口",
                app["admin_url"],
                icon=":material/admin_panel_settings:",
                width="stretch",
            )


def _render_app_grid(apps: tuple[dict[str, str], ...]) -> None:
    for row_start in range(0, len(apps), 3):
        row_apps = apps[row_start : row_start + 3]
        if len(row_apps) == 1 and len(apps) > 1:
            columns = st.columns([1, 1.35, 1], gap="large")
            with columns[1]:
                _render_app_card(row_apps[0])
            continue

        columns = st.columns(len(row_apps), gap="large")
        for column, app in zip(columns, row_apps, strict=True):
            with column:
                _render_app_card(app)


def render_portal() -> None:
    st.set_page_config(
        page_title="Shieldcoating 系統總入口",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    _apply_portal_styles()
    apps = load_portal_apps()

    logo_path = RESOURCE_DIR / "logo.png"
    if logo_path.exists():
        st.image(str(logo_path), width=310)
    else:
        st.markdown(
            '<div class="portal-wordmark">Shield<span>ADVANCED COATINGS</span></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="portal-kicker">WORKSPACE PORTAL</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="portal-title">系統總入口</h1>', unsafe_allow_html=True)
    st.markdown("<div style='height:1.6rem'></div>", unsafe_allow_html=True)

    _render_app_grid(apps)

    st.markdown("<div style='height:0.65rem'></div>", unsafe_allow_html=True)
    st.link_button(
        "查看 Streamlit 官方全部 App",
        OFFICIAL_PROFILE_URL,
        icon=":material/apps:",
        width="stretch",
    )


if __name__ == "__main__":
    render_portal()
