from flask import Blueprint, request, jsonify
from app.services import analyze_text

bp = Blueprint("routes", __name__)

@bp.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    if not data or "text" not in data:
        return jsonify({"error": "No text provided"}), 400
    result = analyze_text(data["text"])
    return jsonify(result)