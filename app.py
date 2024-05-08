from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
import Model as mld

app = Flask(__name__)

UPLOAD_FOLDER = 'uploaded_pdf'  # Directory to save uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarizer' ,methods = ['GET','POST'])
def summarizer():
    result = None
    uploaded_pdf = None
    
    if request.method == 'POST':
        input_text = request.form.get('input_textarea')
        pdf_file = request.files.get('upload-doc')

        if pdf_file:
            uploaded_pdf = pdf_file
            pdf_filename = secure_filename(uploaded_pdf.filename)
            pdf_file.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename))

            # Call generate_summary with the uploaded PDF file
            result = mld.summarize(pdf_file=uploaded_pdf)
        elif input_text:
            # Call generate_summary with the input text
            result = mld.summarize(input_text=input_text)

    return render_template('summarizer.html',result=result)

@app.route('/q_and_a_bot')
def qa():
    return render_template('qa.html')

if __name__ == '__main__':
    # Create the upload directory if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
