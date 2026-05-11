import streamlit as st
from services.auth_service import find_user_by_email, register_user, validate_login


def render_welcome_page(data_manager):
    users = data_manager.load_users()
    sessions = data_manager.load_sessions()
    claims = data_manager.load_claims()

    st.title("Campus Collab Phase 2")
    st.write("A refactored app for study sessions, event needs, and contribution tracking.")

    open_count = 0
    for session in sessions:
        if session["status"] == "Open":
            open_count += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("Open Sessions", open_count)
    col2.metric("Users", len(users))
    col3.metric("Claims", len(claims))

    left, right = st.columns([2, 1])
    with left:
        with st.container(border=True):
            st.markdown("### How it works")
            st.write("Hosts create sessions and list items they still need.")
            st.write("Contributors browse sessions and claim something they will bring.")
    with right:
        with st.container(border=True):
            st.markdown("### Test Accounts")
            st.write("Host: host@udel.edu / host123")
            st.write("Contributor: student@udel.edu / student123")


def render_register_page(data_manager):
    users = data_manager.load_users()

    st.title("Register")
    with st.container(border=True):
        full_name = st.text_input("Full Name", key="register_full_name")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        role = st.selectbox("Role", ["Select a role", "Host", "Contributor"], key="register_role")

        if st.button("Create Account", type="primary", use_container_width=True):
            if full_name.strip() == "" or email.strip() == "" or password.strip() == "" or role == "Select a role":
                st.warning("All fields are required.")
            elif find_user_by_email(users, email) is not None:
                st.error("That email is already registered.")
            else:
                users = register_user(users, full_name, email, password, role)
                data_manager.save_users(users)
                st.success("Account created successfully.")
                st.session_state["page"] = "Log In"
                st.rerun()


def render_login_page(data_manager):
    users = data_manager.load_users()

    st.title("Log In")
    top_left, top_right = st.columns([2, 1])

    with top_left:
        with st.container(border=True):
            login_email = st.text_input("Email", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")

            if st.button("Log In", type="primary", use_container_width=True):
                user = validate_login(users, login_email, login_password)
                if login_email.strip() == "" or login_password.strip() == "":
                    st.warning("Email and password are required.")
                elif user is None:
                    st.error("Invalid credentials.")
                else:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user
                    st.session_state["role"] = user["role"]
                    st.session_state["selected_session_id"] = ""
                    st.session_state["selected_claim_id"] = ""

                    if user["role"] == "Host":
                        st.session_state["page"] = "Host Dashboard"
                    else:
                        st.session_state["page"] = "Contributor Dashboard"
                    st.rerun()

    with top_right:
        with st.container(border=True):
            st.markdown("### Test Accounts")
            st.write("Host")
            st.code("Email: host@udel.edu\nPassword: host123")
            st.write("Contributor")
            st.code("Email: student@udel.edu\nPassword: student123")
