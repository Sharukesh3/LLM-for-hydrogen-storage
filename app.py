from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarizer')
def summarizer():
    return render_template('summarizer.html')

@app.route('/q_and_a_bot')
def qa():
    return render_template('qa.html')

if __name__ == '__main__':
    app.run(debug=True)
