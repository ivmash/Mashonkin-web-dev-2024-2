from flask import Flask, render_template, request, make_response
import re

app = Flask(__name__)
application = app


@app.route('/')
def index():
    url = request.url
    return render_template('index.html', url=url)

@app.route('/args')
def args():
    return render_template('args.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/cookies')
def cookies():
    response = make_response(render_template('cookies.html'))
    if "User"  not in request.cookies:
        response.set_cookie("User","Hello World!")
    else:
        response.delete_cookie("User")
    return response

@app.route("/form", methods = ["POST", "GET"])
def form():
    return render_template("forms.html")

@app.route("/phone", methods = ["POST", "GET"])
def phone():
    error = ''
    number = request.form.get('number')
    if request.method == "POST":
        ns = "".join([i if '0' <= i <= '9' else '' for i in number])
        n_count = len(ns)
        
        if (number.startswith("+7") or number.startswith("8")) and n_count != 11:
            error = 'Номер должен содержать 11 цифр'

        if not number.startswith("+7") and not number.startswith("8") and n_count != 10:
            error = 'Номер должен содержать 10 цифр'
        
        for c in number:
            if c not in "0123456789 ()-.+":
                error = "Номер содержит недопустимые символы"

        if number.startswith("+7") or number.startswith("8"):
            number = f"+7 ({ns[1:4]}) {ns[4:7]}-{ns[7:9]}-{ns[9:]}"
        else:
            number = f"{ns[0:3]}.{ns[3:6]}.{ns[6:8]}.{ns[8:]}"

    return render_template("phone.html", error=error, number=number)
