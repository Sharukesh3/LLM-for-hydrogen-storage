from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import Model as mld
from uuid import uuid4
import Model_QA as mldq

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_pdf'  # Directory to save uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Uploaded_pdf_path = "C:\\familyfolders\\profolders\\Collage stuff\\Sem 2 project\\MI\\uploaded_pdf\\"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarizer', methods=['GET', 'POST'])
def summarizer():
    result = None
    uploaded_pdf = None
    uploaded_files = []  # Initialize an empty list to store uploaded filenames

    if request.method == 'POST':
        input_text = request.form.get('input_textarea')
        pdf_file = request.files.get('upload-doc')

        if pdf_file:
            uploaded_pdf = pdf_file
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))
            uploaded_files.append(pdf_filename)  # Add the filename to the list

            # Call generate_summary with the uploaded PDF file
            result = mld.summarize(pdf_file=Uploaded_pdf_path + pdf_filename)
        elif input_text:
            # Call generate_summary with the input text
            result = mld.summarize(input_text=input_text)

    return render_template('summarizer.html', result=result, uploaded_files=uploaded_files)

@app.route('/q_and_a_bot', methods=['GET', 'POST'])
def qa():
    if request.method == 'POST':
        pdf_file = request.files.get('upload-doc')
        if pdf_file:
            pdf_filename = secure_filename(pdf_file.filename)
            pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))
            # Add any additional processing for the uploaded PDF here

    return render_template('qa.html')

# Endpoint to start a new chat session
@app.route('/new_session')
def new_session():
    session_id = str(uuid4())  # Generate a unique session ID
    return jsonify({"session_id": session_id})

# Endpoint to handle user messages and generate bot responses
@app.route('/chat/<session_id>', methods=['POST'])
def chat(session_id):
    data = request.get_json()
    message = data.get('message', '')
    # Process the user message and generate a bot response
    response = mldq.answer(message)
    return jsonify({"response": response})

if __name__ == '__main__':
    # Create the upload directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)