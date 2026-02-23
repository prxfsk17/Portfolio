import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import ContactForm
from notify import Notify
from modules.morse import MorseConverter

projects = [

    {
        "title": "Weather App",
        "description": "Flask weather application",
        "image": "project1.png",
        "github": "https://github.com/prxfsk17",
        "slug": "weather"
    },

    {
        "title": "Telegram Bot",
        "description": "Telegram bot",
        "image": "project2.png",
        "github": "https://github.com/prxfsk17",
        "slug": "telegram"
    },

    {
        "title": "Morse-code cipher",
        "description": "Convert text to Morse code and vice versa",
        "image": "morse.png",
        "technologies": "Python, OOP",
        'details': 'Represents a python class. Objects of this class can be Morse code encoders or decoders',
        'features': ['Text to Morse conversion', 'Morse to text conversion'],
        "github": "https://github.com/prxfsk17/Portfolio/blob/master/modules/morse.py",
        "slug": "morse"
    },
]

notifier = Notify()
cipher = MorseConverter("cipher")
decipher = MorseConverter("decipher")

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET", "devkey")

@app.route("/")
def home():
    return render_template("about.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html", projects=projects)

@app.route("/project/<slug>")
def project_page(slug):
    project = None
    for p in projects:
        if p["slug"] == slug:
            project = p
            break
    return render_template("project.html", project=project)

@app.route("/demo/morse", methods=["POST", "GET"])
def morse():
    result = None
    error = None

    if request.method == 'POST':
        text = request.form.get('text', '')
        action = request.form.get('action', 'encrypt')

        try:
            if action == 'encrypt':
                result = cipher.operate(text)
            else:
                result = decipher.operate(text)
        except Exception as e:
            error=e

    return render_template('demo/morse.html', result=result, error=error)

@app.route("/contact", methods=["POST", "GET"])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        result = notifier.send_message(
            form.email.data,
            form.subject.data,
            form.message.data
        )
        flash(result)
        return redirect(url_for("contact"))
    return render_template("contact.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)