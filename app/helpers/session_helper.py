"""Helper functions for session related tasks"""
import re


def extract_session_id(session_str: str) -> str:
    """Extract session id from session string"""
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(0)
        return extracted_string

    return ""
