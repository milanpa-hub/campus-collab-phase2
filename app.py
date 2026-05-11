import streamlit as st  # type: ignore[import]

from data_layer.data_manager import DataManager
from services.ai_service import AIChatAssistant
from ui.auth_pages import render_login_page, render_register_page, render_welcome_page
from ui.host_pages import render_create_session_page, render_host_dashboard_page
from ui.contributor_pages import (
    render_browse_sessions_page,
    render_contributor_dashboard_page,
    render_my_claims_page,
)

st.set_page_config(page_title="Campus Collab Phase 2", layout="wide", initial_sidebar_state="expanded")


def init_session_state():
    defaults = {
        "logged_in": False,
        "user": None,
        "role": "",
        "page": "Welcome",
        "selected_session_id": "",
        "selected_claim_id": "",
        "host_chat_messages": [
            {
                "role": "assistant",
                "content": "Hi! I can help summarize missing items, improve event descriptions, and explain claim activity."
            }
        ],
        "contributor_chat_messages": [
            {
                "role": "assistant",
                "content": "Hi! I can help summarize open events, tell you what still needs items, and explain your claims."
            }
        ],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_sidebar():
    with st.sidebar:
        st.markdown("## Campus Collab")
        st.caption("Phase 2: Refactored + AI Assistant")

        if st.session_state["logged_in"]:
            st.success(f"Logged in as {st.session_state['user']['full_name']}")
            st.caption(f"Role: {st.session_state['role']}")
            st.divider()

            if st.session_state["role"] == "Host":
                if st.button("Host Dashboard", use_container_width=True):
                    st.session_state["page"] = "Host Dashboard"
                    st.rerun()
                if st.button("Create Session", use_container_width=True):
                    st.session_state["page"] = "Create Session"
                    st.rerun()

            if st.session_state["role"] == "Contributor":
                if st.button("Contributor Dashboard", use_container_width=True):
                    st.session_state["page"] = "Contributor Dashboard"
                    st.rerun()
                if st.button("Browse Sessions", use_container_width=True):
                    st.session_state["page"] = "Browse Sessions"
                    st.rerun()
                if st.button("My Contributions", use_container_width=True):
                    st.session_state["page"] = "My Contributions"
                    st.rerun()

            st.divider()
            if st.button("Log Out", type="primary", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["user"] = None
                st.session_state["role"] = ""
                st.session_state["page"] = "Welcome"
                st.session_state["selected_session_id"] = ""
                st.session_state["selected_claim_id"] = ""
                st.rerun()
        else:
            if st.button("Welcome", use_container_width=True):
                st.session_state["page"] = "Welcome"
                st.rerun()
            if st.button("Register", use_container_width=True):
                st.session_state["page"] = "Register"
                st.rerun()
            if st.button("Log In", use_container_width=True):
                st.session_state["page"] = "Log In"
                st.rerun()


def main():
    init_session_state()

    data_manager = DataManager("data")
    data_manager.ensure_sample_data()

    ai_assistant = AIChatAssistant()

    render_sidebar()

    if not st.session_state["logged_in"] and st.session_state["page"] == "Welcome":
        render_welcome_page(data_manager)

    elif not st.session_state["logged_in"] and st.session_state["page"] == "Register":
        render_register_page(data_manager)

    elif not st.session_state["logged_in"] and st.session_state["page"] == "Log In":
        render_login_page(data_manager)

    elif st.session_state["logged_in"] and st.session_state["role"] == "Host" and st.session_state["page"] == "Host Dashboard":
        render_host_dashboard_page(data_manager, ai_assistant)

    elif st.session_state["logged_in"] and st.session_state["role"] == "Host" and st.session_state["page"] == "Create Session":
        render_create_session_page(data_manager)

    elif st.session_state["logged_in"] and st.session_state["role"] == "Contributor" and st.session_state["page"] == "Contributor Dashboard":
        render_contributor_dashboard_page(data_manager)

    elif st.session_state["logged_in"] and st.session_state["role"] == "Contributor" and st.session_state["page"] == "Browse Sessions":
        render_browse_sessions_page(data_manager)

    elif st.session_state["logged_in"] and st.session_state["role"] == "Contributor" and st.session_state["page"] == "My Contributions":
        render_my_claims_page(data_manager, ai_assistant)

    else:
        st.title("Campus Collab")
        st.info("Use the sidebar to continue.")


if __name__ == "__main__":
    main()
