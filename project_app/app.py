from flask import Flask, render_template, request


app= Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/results', methods=['GET'])
def search_results():
    ss= request.args.get('search_terms')

    return render_template('search_results.html', search_string= ss)