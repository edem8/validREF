from flask import Flask, jsonify, request, redirect, url_for

from flask_cors import CORS
from formats.apa import extract_apa_citations
from ai import ai


import pandas as pd


app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Welcome to the validRef Microservice"})


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    style = request.form["style"]

    """Save the pdf file """
    save_path = f"./uploads/{file.filename}"
    with open(save_path, "wb+") as destination:
        destination.write(file.read())

    """extract citations"""
    citations = []
    if style == "APA 7th edition":

        citations = extract_apa_citations(save_path)
        valid, invalid = ai(citations)

    elif style == "MLA edition":
        pass

    """return a 200 response"""
    response = (
        jsonify(
            {
                "filename": f"{file.filename}",
                "style": f"{style}",
                "citations": citations,
                "Total": len(citations),
                "valid": valid,
                "valid count": len(valid),
                "invalid": invalid,
                "invlaid count": len(invalid),
            }
        ),
        200,
    )

    return response


if __name__ == "__main__":
    app.run(debug=True)
