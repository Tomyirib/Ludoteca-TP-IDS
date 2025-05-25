from flask import Flask, render_template, jsonify, url_for

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'

@app.route('/')
def index():
    return render_template('index.html', brand=BRAND)

@app.route('/generic')
def generic():
    return render_template('generic.html', brand=BRAND)

if __name__ == '__main__':
    app.run(debug=True, port=8080)