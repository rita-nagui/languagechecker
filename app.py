from flask import Flask, request, render_template
from model import LangCheckerModule

app = Flask(__name__)
lang_checker_module = LangCheckerModule()

# routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/type', methods=['POST', 'GET'])
def text_check():
    if request.method=='POST':
        text = request.form['text']
        text_correct_spelling = lang_checker_module.correct_spelling(text)
        text_correct_grammar = lang_checker_module.correct_grammar(text)
        text_no_mistakes = (text == text_correct_spelling)
        return render_template('index.html',
                               text_correct_spelling=text_correct_spelling,
                               text_correct_grammar=text_correct_grammar,
                               text_no_mistakes=text_no_mistakes)

@app.route('/upload', methods=['POST', 'GET'])
def file_check():
    if request.method == 'POST':
        file = request.files['file']
        readable_file = file.read().decode('utf-8', errors='ignore').strip().replace('\r\n', '\n').replace('\r', '\n')
        if not file.filename.endswith('.txt'):
            return "Only .txt files are supported", 400
        file_correct_spelling = lang_checker_module.correct_spelling(readable_file)
        file_correct_grammar = lang_checker_module.correct_grammar(readable_file)
        file_no_mistakes = (readable_file == file_correct_spelling)
        return render_template('index.html',
                               file_correct_spelling=file_correct_spelling,
                               file_correct_grammar=file_correct_grammar,
                               file_no_mistakes=file_no_mistakes)

if __name__ == "__main__":
    app.run(debug=True)