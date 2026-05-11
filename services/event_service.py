from datetime import datetime
import uuid
from models.event import Event
from models.need import Need
from models.claim import Claim


def get_host_sessions(sessions, host_id):
    return [session for session in sessions if session["host_id"] == host_id]


def get_contributor_claims(claims, contributor_id):
    return [claim for claim in claims if claim["contributor_id"] == contributor_id]


def get_open_sessions(sessions):
    return [session for session in sessions if session["status"] == "Open"]


def create_session_with_need(
    sessions,
    needs,
    host_id,
    title,
    category,
    session_date,
    session_time,
    location,
    description,
    need_item,
    need_quantity,
    need_notes
):
    new_session_id = str(uuid.uuid4())
    new_event = Event(
        session_id=new_session_id,
        host_id=host_id,
        title=title.strip(),
        category=category,
        date=str(session_date),
        time=session_time.strip(),
        location=location.strip(),
        description=description.strip(),
        status="Open",
        created_at=str(datetime.now())
    )
    sessions.append(new_event.to_dict())

    new_need = Need(
        need_id=str(uuid.uuid4()),
        session_id=new_session_id,
        item_name=need_item.strip(),
        quantity_needed=int(need_quantity),
        quantity_claimed=0,
        notes=need_notes.strip()
    )
    needs.append(new_need.to_dict())
    return sessions, needs


def create_claim(claims, needs, selected_need, contributor_id, session_id):
    selected_need["quantity_claimed"] = int(selected_need["quantity_claimed"]) + 1
    new_claim = Claim(
        claim_id=str(uuid.uuid4()),
        need_id=selected_need["need_id"],
        session_id=session_id,
        contributor_id=contributor_id,
        claimed_item=selected_need["item_name"],
        status="Claimed",
        claimed_at=str(datetime.now())
    )
    claims.append(new_claim.to_dict())
    return claims, needs


def delete_claim(claims, needs, claim_id):
    selected_claim = None
    for claim in claims:
        if claim["claim_id"] == claim_id:
            selected_claim = claim
            break

    if selected_claim is not None:
        for need in needs:
            if need["need_id"] == selected_claim["need_id"] and int(need["quantity_claimed"]) > 0:
                need["quantity_claimed"] = int(need["quantity_claimed"]) - 1

    claims = [claim for claim in claims if claim["claim_id"] != claim_id]
    return claims, needs


def update_claim_status(claims, claim_id, new_status):
    for claim in claims:
        if claim["claim_id"] == claim_id:
            claim["status"] = new_status
            break
    return claims
