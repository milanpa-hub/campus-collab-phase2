import streamlit as st
from services.event_service import (
    create_claim,
    delete_claim,
    get_contributor_claims,
    get_open_sessions,
    update_claim_status,
)


def render_contributor_dashboard_page(data_manager):
    sessions = data_manager.load_sessions()
    claims = data_manager.load_claims()

    st.title("Contributor Dashboard")
    my_claims = get_contributor_claims(claims, st.session_state["user"]["user_id"])
    open_sessions = get_open_sessions(sessions)

    col1, col2 = st.columns(2)
    col1.metric("My Claims", len(my_claims))
    col2.metric("Open Sessions", len(open_sessions))

    lower_left, lower_right = st.columns(2)
    with lower_left:
        with st.container(border=True):
            st.markdown("### My Recent Claims")
            if len(my_claims) == 0:
                st.info("You have not claimed anything yet.")
            else:
                rows = []
                for claim in my_claims:
                    session_title = "Unknown"
                    for session in sessions:
                        if session["session_id"] == claim["session_id"]:
                            session_title = session["title"]
                            break
                    rows.append({
                        "Session": session_title,
                        "Item": claim["claimed_item"],
                        "Status": claim["status"],
                    })
                st.dataframe(rows, use_container_width=True)

    with lower_right:
        with st.container(border=True):
            st.markdown("### Open Sessions")
            if len(open_sessions) == 0:
                st.info("There are no open sessions right now.")
            else:
                rows = []
                for session in open_sessions:
                    rows.append({
                        "Title": session["title"],
                        "Date": session["date"],
                        "Location": session["location"],
                    })
                st.dataframe(rows, use_container_width=True)


def render_browse_sessions_page(data_manager):
    sessions = data_manager.load_sessions()
    needs = data_manager.load_needs()
    claims = data_manager.load_claims()

    st.title("Browse Sessions")
    open_sessions = get_open_sessions(sessions)

    if len(open_sessions) == 0:
        st.warning("There are no open sessions right now.")
        return

    options = []
    for session in open_sessions:
        options.append(f"{session['title']} | {session['session_id']}")

    selected_label = st.selectbox("Select a session", options, key="browse_session_select")
    session_id = selected_label.split(" | ")[-1]

    selected_session = None
    for session in open_sessions:
        if session["session_id"] == session_id:
            selected_session = session
            break

    if selected_session is None:
        return

    left, right = st.columns([2, 1])
    with left:
        with st.container(border=True):
            st.markdown(f"### {selected_session['title']}")
            st.write(f"**Date:** {selected_session['date']}")
            st.write(f"**Time:** {selected_session.get('time', '')}")
            st.write(f"**Location:** {selected_session['location']}")
            st.write(f"**Description:** {selected_session['description']}")
    with right:
        with st.container(border=True):
            available_count = 0
            for need in needs:
                if need["session_id"] == session_id:
                    remaining = int(need["quantity_needed"]) - int(need["quantity_claimed"])
                    if remaining > 0:
                        available_count += 1
            st.metric("Available Item Types", available_count)

    available_needs = []
    display_rows = []
    labels = []
    for need in needs:
        if need["session_id"] == session_id:
            remaining = int(need["quantity_needed"]) - int(need["quantity_claimed"])
            if remaining > 0:
                available_needs.append(need)
                display_rows.append({
                    "Item": need["item_name"],
                    "Remaining": remaining,
                    "Notes": need.get("notes", "")
                })
                labels.append(f"{need['item_name']} | {remaining} left | {need['need_id']}")

    st.markdown("### Available Items to Claim")
    if len(available_needs) == 0:
        st.info("Everything for this session has already been claimed.")
        return

    st.dataframe(display_rows, use_container_width=True)
    selected_need_label = st.selectbox("Choose an item to bring", labels, key="browse_need_select")
    selected_need_id = selected_need_label.split(" | ")[-1]

    selected_need = None
    for need in available_needs:
        if need["need_id"] == selected_need_id:
            selected_need = need
            break

    if st.button("Claim This Item", type="primary", use_container_width=True):
        already_claimed_same_item = False
        for claim in claims:
            if claim["contributor_id"] == st.session_state["user"]["user_id"] and claim["need_id"] == selected_need_id:
                already_claimed_same_item = True

        if already_claimed_same_item:
            st.warning("You already claimed this exact item.")
        else:
            claims, needs = create_claim(claims, needs, selected_need, st.session_state["user"]["user_id"], session_id)
            data_manager.save_claims(claims)
            data_manager.save_needs(needs)
            st.success("Item claimed successfully.")
            st.session_state["page"] = "My Contributions"
            st.rerun()


def render_my_claims_page(data_manager, ai_assistant):
    sessions = data_manager.load_sessions()
    needs = data_manager.load_needs()
    claims = data_manager.load_claims()

    st.title("My Contributions")
    my_claims = get_contributor_claims(claims, st.session_state["user"]["user_id"])

    tab1, tab2 = st.tabs(["Manage Claims", "AI Assistant"])

    with tab1:
        if len(my_claims) == 0:
            st.info("You do not have any claims yet.")
        else:
            rows = []
            for claim in my_claims:
                session_title = "Unknown"
                for session in sessions:
                    if session["session_id"] == claim["session_id"]:
                        session_title = session["title"]
                        break
                rows.append({
                    "Session": session_title,
                    "Item": claim["claimed_item"],
                    "Status": claim["status"],
                })
            st.dataframe(rows, use_container_width=True)

            options = []
            for claim in my_claims:
                options.append(f"{claim['claimed_item']} | {claim['claim_id']}")

            selected_label = st.selectbox("Select a claim", options, key="claims_manage_select")
            claim_id = selected_label.split(" | ")[-1]

            selected_claim = None
            for claim in my_claims:
                if claim["claim_id"] == claim_id:
                    selected_claim = claim
                    break

            if selected_claim:
                with st.container(border=True):
                    st.write(f"**Item:** {selected_claim['claimed_item']}")
                    st.write(f"**Status:** {selected_claim['status']}")

                new_status = st.selectbox(
                    "Update Status",
                    ["Claimed", "Canceled"],
                    index=0 if selected_claim["status"] == "Claimed" else 1,
                    key="claim_status_update_select",
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Update Claim", type="primary", use_container_width=True):
                        claims = update_claim_status(claims, claim_id, new_status)
                        data_manager.save_claims(claims)
                        st.success("Claim updated.")
                        st.rerun()

                with col2:
                    if st.button("Delete Claim", use_container_width=True):
                        claims, needs = delete_claim(claims, needs, claim_id)
                        data_manager.save_claims(claims)
                        data_manager.save_needs(needs)
                        st.success("Claim deleted.")
                        st.rerun()

    with tab2:
        if not ai_assistant.is_available():
            st.warning("OpenAI key not found yet. Add OPENAI_API_KEY to Streamlit secrets to enable the assistant.")

        with st.container(border=True):
            for msg in st.session_state["contributor_chat_messages"]:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])

        prompt = st.chat_input("Ask the contributor assistant...", key="contributor_ai_input")
        if prompt:
            my_claims = get_contributor_claims(claims, st.session_state["user"]["user_id"])
            open_sessions = get_open_sessions(sessions)
            st.session_state["contributor_chat_messages"].append({"role": "user", "content": prompt})
            response = ai_assistant.get_contributor_response(prompt, open_sessions, needs, my_claims)
            st.session_state["contributor_chat_messages"].append({"role": "assistant", "content": response})
            st.rerun()
