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
        "availability": [
            {"start": "2024-06-15T09:00:00", "end": "2024-06-15T17:00:00"}
        ],  # Placeholder availability
        "duration": 60,  # Duration in minutes, adjust as needed
    }

    print(f"Extracted meeting details: {meeting_details}")
    return meeting_details
