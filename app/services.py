import spacy
import re

# Lade das deutsche Modell
nlp = spacy.load("de_core_news_sm")

def analyze_and_anonymize_text(text):
    doc = nlp(text)

    anonymized_text = text  # Originaltext
    replacements = {}

    # Whitelist für Technologien und Begriffe, die erhalten bleiben sollen
    tech_whitelist = {"Angular", "Vue.js", "Node.js", "Lambda", "CloudFront", "AWS", "Knex.js"}
    general_whitelist = {"GitLab", "SSL-Zertifikate", "Server", "Frontend", "Backend"}

    # E-Mail-Muster definieren
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails_found = re.findall(email_pattern, text)

    for email in emails_found:
        placeholder = "[EMAIL]"
        replacements[email] = placeholder
        anonymized_text = anonymized_text.replace(email, placeholder)

    # Adresse (Straße und PLZ) Muster definieren
    address_pattern = r'\b[A-Za-zäöüßÄÖÜ]+(?:\s[A-Za-zäöüßÄÖÜ]+)*\s(?:Str\.|Straße|Platz|Weg|Allee)\s\d{1,5},\s\d{5}\b'
    addresses_found = re.findall(address_pattern, text)

    for address in addresses_found:
        placeholder = "[ADDRESS]"
        replacements[address] = placeholder
        anonymized_text = anonymized_text.replace(address, placeholder)

    # Gehe durch alle erkannte Entitäten von spaCy
    for ent in doc.ents:
        # Überspringe, wenn die Entität in einer Whitelist steht
        if ent.text in tech_whitelist or ent.text in general_whitelist:
            continue

        # Prüfe, ob die Entität anonymisiert werden soll
        if ent.label_ in ["PER", "LOC", "ORG", "EMAIL", "PHONE"]:
            placeholder = f"[{ent.label_}]"
            replacements[ent.text] = placeholder
            anonymized_text = anonymized_text.replace(ent.text, placeholder)

    # Rückgabe des Ergebnisses
    return {
        "tokens": [token.text for token in doc],
        "entities": [{"text": ent.text, "label": ent.label_} for ent in doc.ents],
        "anonymized_text": anonymized_text,
    }