from flask import Blueprint, request, jsonify
from app.services import anonymize_text
import json

bp = Blueprint("routes", __name__)

@bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    result = anonymize_text(data["text"])
    print(json.dumps(result, indent=4))
    return jsonify(result)