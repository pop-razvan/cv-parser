from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from io import BytesIO
import json
import ollama

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@app.route('/api/upload', methods=['POST'])
def upload_cv():
    # Validate file upload
    if 'pdf' not in request.files:
        return jsonify({"error": "No PDF file provided."}), 400
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    # Extract text from PDF using PyPDF2
    try:
        file_data = file.read()
        pdf_file = BytesIO(file_data)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    except Exception as e:
        return jsonify({"error": f"Error reading PDF: {str(e)}"}), 500

    # Create a prompt for Llama3.2:1b to extract skills and experience
    prompt = (
        "Extract a list of skills and experience from the following CV:\n\n"
        f"{text}\n\n"
        "Return the result as JSON with two keys: 'skills' (a list of skills) and 'experience' (a list of experiences)."
    )

    try:
        # Use the Ollama library with model "llama3.2:1b"
        ollama_result = ollama.generate(model="llama3.2:1b", prompt=prompt)
        
        # Convert the GenerateResponse object to a serializable format.
        # If the object has an attribute called 'response', use it.
        if hasattr(ollama_result, 'response'):
            response_text = ollama_result.response
        else:
            response_text = str(ollama_result)

    except Exception as e:
        return jsonify({
            "error": "Error calling Ollama using the Ollama library.",
            "details": str(e)
        }), 500

    # Try to parse the result as JSON; if parsing fails, return it as plain text.
    try:
        parsed_result = json.loads(response_text)
    except Exception as e:
        parsed_result = {"result": response_text}

    return jsonify(parsed_result)

@app.route('/candidates', methods=['POST'])
def find_candidates():
    return 'Find Candidates'

if __name__ == '__main__':
    app.run()