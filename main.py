import os
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import ContactForm
from notify import Notify
from modules.morse import MorseConverter
from modules.webscraping import Currencies

projects = [

    {
        "title": "Top Currencies in Minsk",
        "description": "Find best USD and EUR exchange rates in Minsk banks.",
        "image": "currencies.png",
        "technologies": "BeautifulSoup, Requests, smtplib, OOP",
        "details": "Python class that scrapes top 1-5 currency exchange rates in Minsk and can send results via email using SMTP",
        "features": [
            "USD and EUR rate scraping",
            "Top 1-5 best rates selection",
            "Bank names and currencies",
            "Email reports via SMTP"
        ],
        "github": "https://github.com/prxfsk17/Portfolio/blob/master/modules/webscraping.py",
        "slug": "currencies"
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

load_dotenv()

notifier = Notify()
cipher = MorseConverter("cipher")
decipher = MorseConverter("decipher")
currency_manager = Currencies()

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

@app.route("/demo/currencies", methods=["POST", "GET"])
def currencies():
    result = None
    error = None
    top_selected = 5
    print(132)
    if request.method == "POST":
        try:
            top_selected = request.form.get('top', type=int, default=5)
            result = currency_manager.get_results(top_selected)
        except Exception as e:
            error = str(e)
    return render_template("demo/currencies.html",
                         result=result,
                         error=error,
                         top_selected=top_selected)

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