import streamlit as st
from services.event_service import get_host_sessions


def render_host_dashboard_page(data_manager, ai_assistant):
    sessions = data_manager.load_sessions()
    needs = data_manager.load_needs()
    claims = data_manager.load_claims()

    st.title("Host Dashboard")

    my_sessions = get_host_sessions(sessions, st.session_state["user"]["user_id"])

    total_claims = 0
    total_open_sessions = 0
    for session in my_sessions:
        if session["status"] == "Open":
            total_open_sessions += 1
        for claim in claims:
            if claim["session_id"] == session["session_id"]:
                total_claims += 1

    col1, col2, col3 = st.columns(3)
    col1.metric("My Sessions", len(my_sessions))
    col2.metric("My Open Sessions", total_open_sessions)
    col3.metric("Claims on My Sessions", total_claims)

    tab1, tab2 = st.tabs(["Session Overview", "AI Assistant"])

    with tab1:
        if len(my_sessions) == 0:
            st.info("You have not created any sessions yet.")
        else:
            display_rows = []
            for session in my_sessions:
                display_rows.append({
                    "Title": session["title"],
                    "Category": session.get("category", ""),
                    "Date": session["date"],
                    "Time": session.get("time", ""),
                    "Location": session["location"],
                    "Status": session["status"],
                })
            st.dataframe(display_rows, use_container_width=True)

            session_options = []
            for session in my_sessions:
                session_options.append(f"{session['title']} | {session['session_id']}")

            selected_label = st.selectbox("Select a session", session_options, key="host_dashboard_session_select")
            session_id = selected_label.split(" | ")[-1]

            selected_session = None
            for session in my_sessions:
                if session["session_id"] == session_id:
                    selected_session = session
                    break

            if selected_session:
                detail_col1, detail_col2 = st.columns([2, 1])

                with detail_col1:
                    with st.container(border=True):
                        st.markdown(f"### {selected_session['title']}")
                        st.write(f"**Date:** {selected_session['date']}")
                        st.write(f"**Time:** {selected_session.get('time', '')}")
                        st.write(f"**Location:** {selected_session['location']}")
                        st.write(f"**Description:** {selected_session['description']}")
                        st.write(f"**Status:** {selected_session['status']}")

                with detail_col2:
                    with st.container(border=True):
                        open_need_count = 0
                        for need in needs:
                            if need["session_id"] == session_id:
                                remaining = int(need["quantity_needed"]) - int(need["quantity_claimed"])
                                if remaining > 0:
                                    open_need_count += 1
                        st.metric("Open Need Items", open_need_count)

                need_rows = []
                for need in needs:
                    if need["session_id"] == session_id:
                        need_rows.append({
                            "Item": need["item_name"],
                            "Needed": need["quantity_needed"],
                            "Claimed": need["quantity_claimed"],
                            "Remaining": int(need["quantity_needed"]) - int(need["quantity_claimed"]),
                            "Notes": need.get("notes", "")
                        })

                if len(need_rows) > 0:
                    st.markdown("#### Needs List")
                    st.dataframe(need_rows, use_container_width=True)

    with tab2:
        if not ai_assistant.is_available():
            st.warning("OpenAI key not found yet. Add OPENAI_API_KEY to Streamlit secrets to enable the assistant.")

        with st.container(border=True):
            for msg in st.session_state["host_chat_messages"]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        user_prompt = st.chat_input("Ask the host assistant...", key="host_ai_input")
        if user_prompt:
            st.session_state["host_chat_messages"].append({"role": "user", "content": user_prompt})
            response = ai_assistant.get_host_response(user_prompt, my_sessions, needs, claims)
            st.session_state["host_chat_messages"].append({"role": "assistant", "content": response})
            st.rerun()


def render_create_session_page(data_manager):
    from services.event_service import create_session_with_need

    st.title("Create Session")

    with st.form("create_session_form", clear_on_submit=True):
        title = st.text_input("Session Title")
        category = st.selectbox("Category", ["Study Session", "Club Prep", "Project Work", "Workshop", "Presentation Practice"])
        session_date = st.date_input("Date")
        session_time = st.text_input("Time", placeholder="Example: 7:00 PM")
        location = st.text_input("Location")
        description = st.text_area("Description")
        need_item = st.text_input("Needed Item")
        need_quantity = st.number_input("Needed Quantity", min_value=1, step=1)
        need_notes = st.text_input("Needed Item Notes")
        submitted = st.form_submit_button("Save Session", type="primary", use_container_width=True)

    if submitted:
        if title.strip() == "" or session_time.strip() == "" or location.strip() == "" or need_item.strip() == "":
            st.warning("Title, time, location, and one needed item are required.")
        else:
            sessions = data_manager.load_sessions()
            needs = data_manager.load_needs()
            sessions, needs = create_session_with_need(
                sessions,
                needs,
                st.session_state["user"]["user_id"],
                title,
                category,
                session_date,
                session_time,
                location,
                description,
                need_item,
                need_quantity,
                need_notes
            )
            data_manager.save_sessions(sessions)
            data_manager.save_needs(needs)
            st.success("Session created successfully.")
            st.session_state["page"] = "Host Dashboard"
            st.rerun()
