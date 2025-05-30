from flask import Flask, render_template
import requests

app = Flask(__name__)
BRAND = 'Ludoteca Vapor'

@app.route('/')
def index():
    get_game()
    return render_template('index.html', brand=BRAND)

@app.route('/generic')
def generic():
    return render_template('generic.html', brand=BRAND)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if requests.method == 'POST':
        if 'email_login' in requests.form:
            email = requests.form['email_login']
            password = requests.form['password_login']
        elif 'email_signup' in requests.form:
            email = requests.form['email_signup']
            password = requests.form['password_signup']
            first_name = requests.form['first_name']
            last_name = requests.form['last_name']
    return render_template('login.html', brand=BRAND)

@app.route('/carrito')
def carrito():
    return render_template('carrito.html', brand=BRAND)


def get_game():
    response = requests.get("http://localhost:8080/games/440")

    if response.status_code == 200:
        print(response.json())
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)