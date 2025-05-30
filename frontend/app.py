from flask import Flask, render_template, request
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

@app.route('/login', methods=['GET'])
def login():
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