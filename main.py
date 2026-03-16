import os

import dateutil
from dotenv import load_dotenv
from flask import Flask, render_template, redirect, url_for, flash, request
from forms import ContactForm
from notify import Notify
from modules.morse import MorseConverter
from modules.webscraping import Currencies
from modules.automation import OnlinerParser
from modules.api.main import api_bp

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
        "title": "Cafe and Wifi API",
        "description": "A RESTful API to manage and discover cafes with amenities like WiFi, power sockets, and coffee prices.",
        "image": "postman.png",
        "technologies": "Flask, REST, CRUD, SQLAlchemy, Postman",
        "details": "This project is a fully functional REST API that allows users to perform CRUD operations on a database of cafes. Users can get a list of all cafes, search by location, get a random cafe, add new cafes, update coffee prices, and delete cafes. The API returns clean JSON responses, making it easy to integrate into front-end applications.",
        "features": [
            "GET /all - Retrieve all cafes",
            "GET /search?loc= - Search cafes by location",
            "GET /random - Get a random cafe suggestion",
            "POST /add - Add a new cafe to the database",
            "PATCH /update-price/ - Update coffee price",
            "DELETE /report-closed/ - Delete a cafe (API key required)"
        ],
        "github": "https://github.com/prxfsk17/100DaysOfPython/tree/master/Day%2066",
        "slug": "cafe-api"
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

    {
        "title": "Space Invaders",
        "description": "Classic arcade space shooter with multiple enemy types and progressive difficulty",
        "image": "game.png",
        "technologies": "Python, pygame (pygame-ce), OOP, pygbag",
        "details": "A fully-featured Space Invaders clone with smooth controls, enemy animations, particle effects, and increasing difficulty. Features multiple enemy colors with different point values, shooting enemies, and a starfield background.",
        "features": [
            "Player ship with smooth A/D controls",
            "3 enemy types with unique animations",
            "Enemies shoot back at player",
            "Progressive difficulty (5+ levels)",
            "Score and lives system",
            "Particle starfield background",
            "Game over and restart functionality"
        ],
        "github": "https://github.com/prxfsk17/100DaysOfPython/tree/master/Day%2095",
        "slug": "space-invaders"
    },
    {
        "title": "Onliner Catalog Parser",
        "description": "Automated product search and price analysis on Onliner.by using Selenium",
        "image": "automation.png",
        "technologies": "Python, Selenium, BeautifulSoup, NumPy, OOP",
        "details": "A powerful web automation tool that searches for products on Onliner.by, extracts AI descriptions, and provides comprehensive price statistics including min, max, mean, and median prices from all available offers.",
        "features": [
            "Automated product search by query",
            "AI product description extraction",
            "Comprehensive price statistics",
            "Smart cookie handling",
            "Retry mechanism for stable clicks",
            "Price parsing from multiple offers",
            "Headless mode support",
            "Clean OOP architecture with dataclasses"
        ],
        "github": "https://github.com/prxfsk17/Portfolio/blob/master/modules/automation.py",
        "slug": "automation"
    },
    {
        "title": "Interactive API Website (F1 Theme)",
        "description": "A dynamic website that fetches and displays data from a public API, featuring interactive elements and custom backend logic.",
        "image": "api_project.png",
        "technologies": "Flask, HTML, CSS, Bootstrap, Jinja, Requests",
        "details": "This project is a self-contained web application built with Flask. It serves multiple HTML pages, utilizes helper functions to call external APIs, processes the data, and presents it in a user-friendly interface. The project demonstrates full-stack skills, from backend server logic to frontend templating.",
        "features": [
            "Custom Flask server with multiple routes",
            "Integration with external APIs",
            "Dynamic HTML pages using Jinja templating",
            "Data processing and visualization",
            "Modular code structure with separate helper files",
            "Responsive design with Bootstrap"
        ],
        "github": "https://github.com/prxfsk17/100DaysOfPython/tree/master/Day%2096",
        "slug": "api-website"
    }
]

load_dotenv()

notifier = Notify()
cipher = MorseConverter("cipher")
decipher = MorseConverter("decipher")
currency_manager = Currencies()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET", "devkey")

@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
    native = date.replace(tzinfo=None)
    format = '%b %d, %Y - %H:%M'
    return native.strftime(format)

@app.template_filter('safe_int')
def safe_int_filter(value):
    try:
        return int(value) if value is not None else 0
    except:
        return 0

@app.template_filter('to_datetime')
def to_datetime_filter(date_string):
    if isinstance(date_string, str):
        try:
            from datetime import datetime
            return datetime.strptime(date_string, '%Y-%m-%d')
        except:
            return None
    return date_string

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

@app.route("/demo/currencies", methods=["POST", "GET"], strict_slashes=False)
def currencies():
    result = None
    error = None
    top_selected = 5
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

@app.route("/demo/space-invaders", methods=["GET"])
def space_invaders():
    return render_template("demo/space_invaders.html")

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

@app.route("/demo/cafe-api", methods=["POST", "GET"])
def postman():
    return redirect("https://documenter.getpostman.com/view/50726073/2sB3dSP8Yv")

@app.route("/demo/automation", methods=["GET", "POST"])
def automation():
    result = None
    error = None
    query = None

    if request.method == "POST":
        query = request.form.get("product", "").strip()

        if not query:
            error = "Please enter a product name"
        else:
            try:
                parser = OnlinerParser(headless=True, detach=False)

                try:
                    product = parser.search_product(query)

                    if product and product.price_stats:
                        result = {
                            "name": product.name,
                            "url": product.url,
                            "ai_description": product.ai_description,
                            "price_stats": product.price_stats
                        }
                    else:
                        error = "Could not find price information for this product"
                finally:
                    parser.close()

            except Exception as e:
                error = f"An error occurred: {str(e)}"
    return render_template("demo/automation.html",
                           result=result,
                           error=error,
                           query=query)

app.register_blueprint(api_bp, url_prefix='/demo/api-website')

if __name__ == "__main__":
    app.run(debug=True)