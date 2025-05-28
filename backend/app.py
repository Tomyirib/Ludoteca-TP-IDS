from flask import Flask, render_template, jsonify, url_for, request

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'

@app.route('/')
def index():
    return render_template('index.html', brand=BRAND)

@app.route('/generic')
def generic():
    return render_template('generic.html', brand=BRAND)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'email_login' in request.form:
            email = request.form['email_login']
            password = request.form['password_login']
        elif 'email_signup' in request.form:
            email = request.form['email_signup']
            password = request.form['password_signup']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
    return render_template('login.html', brand=BRAND)

@app.route('/carrito')
def carrito():
    return render_template('carrito.html', brand=BRAND)


if __name__ == '__main__':
    app.run(debug=True, port=8080)