import nltk
import spacy


def init_nlp():
    nltk.download("punkt")
    nlp = spacy.load("en_core_web_sm")
    return nlp


def extract_meeting_details(email_content):
    nlp = init_nlp()
    doc = nlp(email_content)
    # Extract details from email content
    meeting_details = {
        # Extracted details (for now, it's a placeholder)
        "date": "2024-06-15",
        "time": "10:00:00",
    }
    return meeting_details
