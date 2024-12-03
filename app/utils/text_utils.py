import spacy

def analyze_text(text):
    """
    Analyzes the given text and returns tokens, entities, and sentences.

    Args:
        text (str): Input text to analyze.

    Returns:
        dict: Analysis results containing tokens, entities, and sentences.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    return {
        "tokens": [token.text for token in doc],
        "entities": [(ent.text, ent.label_) for ent in doc.ents],
        "sentences": [sent.text for sent in doc.sents]
    }