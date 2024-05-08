from flask import Flask, render_template, request

def generate_summary(input_text):
    # Your text summarization logic here
    summary = "This is a sample summary for the input text."
    return summary

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarizer' ,methods = ['GET','POST'])
def summarizer():
    result = None
    if request.method == 'POST':
        input_text = request.form.get('input_textarea')
        # Process the input_text and generate the summary
        result = generate_summary(input_text)
    return render_template('summarizer.html',result=result)

@app.route('/q_and_a_bot')
def qa():
    return render_template('qa.html')

if __name__ == '__main__':
    app.run(debug=True)
