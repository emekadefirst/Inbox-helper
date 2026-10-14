ALIASES = {
    "from_email": {"from", "from_email", "email", "mail", "sender"},
    "candidate_name": {"candidate_name", "name", "candidate", "full_name"},
    "subject": {"subject"},
    "message": {"message", "body", "text"},
    "job_title": {"job_title", "job", "position", "role", "title"},
    "resume_url": {"resume_url", "resume", "resume_link", "cv"},
    "cover_letter_url": {"cover_letter_url", "cover_letter", "coverletter", "cover_letter_link"},
}
_LOOKUP = {alias: field for field, names in ALIASES.items() for alias in names}

def normalize_row(raw: dict) -> dict:
    out = {}
    for key, value in raw.items():
        field = _LOOKUP.get(str(key).strip().lower().replace(" ", "_"))
        if not field:
            continue                                           
        if isinstance(value, str):
            value = value.strip() or None
        out[field] = value
    return out

