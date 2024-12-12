import re
import spacy
from spacy.tokens import Span
from .tech_whitelist import tech_whitelist  # Whitelist importieren

nlp = spacy.load("de_core_news_sm")

def preprocess_text(text):
    """Entfernt unerwünschte Zeichen und formatiert den Text."""
    unwanted_chars = ['\u2022', '\u25e6', '\u2023', '\uf0b7']
    for char in unwanted_chars:
        text = text.replace(char, '')
    return text.strip()

def anonymize_phone_numbers(text):
    """Entfernt zuverlässig alle Telefonnummern."""
    phone_pattern = r'''
        (?:(?:\+|00)49)?           # Deutsche Landesvorwahl optional
        [-.\s]?\(?\d{2,4}\)?       # Optionale Vorwahl mit Klammern
        [-.\s]?\d{2,5}             # Hauptnummer-Teil 1
        [-.\s]?\d{2,5}             # Hauptnummer-Teil 2
        (?:[-.\s]?\d{1,5})?        # Optionale Endziffern
        \b                         # Wortgrenze
    '''
    return re.sub(phone_pattern, '[TELEFONNUMMER ENTFERNT]', text, flags=re.VERBOSE)

def anonymize_email_addresses(text):
    """Entfernt E-Mail-Adressen aus dem Text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.sub(email_pattern, '[E-MAIL ENTFERNT]', text)

def anonymize_personal_data_with_spacy(text):
    """Anonymisiert personenbezogene Daten mit spaCy."""
    doc = nlp(text)
    new_ents = []
    replacements = {}
    first_person = None

    for ent in doc.ents:
        if ent.text in tech_whitelist:
            # Whitelisted-Begriffe überspringen
            new_ents.append(Span(doc, ent.start, ent.end, label="MISC"))
            continue

        if ent.label_ == "PER" and not first_person:
            first_person = ent.text  # Speichere den ersten Namen

        placeholder = {
            "PER": "[NAME ENTFERNT]",
            "LOC": "[ORT ENTFERNT]",
            "ORG": "[ORGANISATION ENTFERNT]",
            "GPE": "[ORT ENTFERNT]"
        }.get(ent.label_, None)

        if placeholder:
            replacements[ent.text] = placeholder
            text = text.replace(ent.text, placeholder)

    doc.ents = new_ents
    return text, first_person

def anonymize_text(text):
    """Hauptfunktion zur Anonymisierung."""
    text = preprocess_text(text)
    text = anonymize_phone_numbers(text)  # Telefonnummern entfernen
    text = anonymize_email_addresses(text)  # E-Mails entfernen
    text, first_person = anonymize_personal_data_with_spacy(text)  # spaCy-Daten anonymisieren
    return {
        "anonymized_text": text.strip(),
        "first_person": first_person,
    }