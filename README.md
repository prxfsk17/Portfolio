# Developer Portfolio (Flask)
![CI](https://github.com/prxfsk17/Portfolio/actions/workflows/ci.yml/badge.svg)

A personal portfolio website built with Flask. It presents my background, a catalog of projects with detail pages, a contact form, and several interactive demos that run in the browser.

## Features

- **About / Portfolio / Project pages** - project catalog rendered with Jinja templates
- **Contact form** - validation with Flask-WTF, messages delivered by email over SMTP
- **Morse code translator** - text to Morse and back
- **Currency rates scraper** - collects USD/EUR rates from bank pages (Requests + BeautifulSoup) and shows the best offers
- **Onliner price parser** - Selenium automation that searches a product and computes price statistics (min / max / mean / median). Needs Chrome, runs locally only
- **F1 data explorer** - a Flask Blueprint that fetches circuits, teams and drivers from the API-Sports Formula 1 API, with an in-memory cache and built-in sample data as a fallback
- **Space Invaders** - a pygame game compiled to WebAssembly with pygbag and embedded in the page

## Tech stack

Python, Flask, Jinja2, Flask-WTF / WTForms, Requests, BeautifulSoup, Selenium, NumPy, Bootstrap 5

## Project structure

```
.
├── main.py              # Flask app, routes, project catalog
├── forms.py             # Contact form (Flask-WTF)
├── notify.py            # Email sending via SMTP
├── modules/
│   ├── api/             # F1 data explorer (Flask Blueprint)
│   ├── game/            # Space Invaders source (pygame)
│   ├── automation.py    # Selenium product price parser
│   ├── morse.py         # Morse code converter
│   └── webscraping.py   # Currency rates scraper
├── static/              # CSS, images, WebAssembly game build
└── templates/           # Jinja templates
```

## Getting started

Requirements: Python 3.11+; Chrome is needed only for the Onliner parser demo.

```bash
git clone https://github.com/prxfsk17/Portfolio.git
cd Portfolio
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env    # then fill in the values
python main.py
```

Open http://127.0.0.1:5000

### With Docker

```bash
cp .env.example .env    # fill in the values
docker compose up --build
```
Open http://localhost:8000. The Selenium-based Onliner demo is disabled in the container (it needs a local Chrome).

### Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Environment variables

| Variable | Used for |
|---|---|
| `SECRET` | Flask secret key |
| `SENDER_MAIL`, `PASSWORD_MAIL` | Gmail account (app password) used to send contact-form messages |
| `RECIPIENT_MAIL` | Address that receives the messages |
| `SCRAPING_PAGE` | URL of the page with bank exchange rates |
| `F1_KEY` | API-Sports API key |
| `F1_URL_CIRC`, `F1_URL_TEAMS`, `F1_URL_DRIVERS` | API-Sports Formula 1 endpoints |

The site starts without a `.env` file, but the contact form, currency scraper and F1 live data need the values above. Without an F1 key the explorer falls back to a small built-in sample data set.

## Known limitations

- The Onliner parser depends on the current markup of the target site (XPath selectors) and may break when the site changes.
- The F1 cache is in memory and is not shared between processes.

## Roadmap

- [x] Dockerfile and docker-compose
- [x] Automated tests and CI with GitHub Actions
- [ ] Public deployment

## Author

Aliaksandr Haiko - [LinkedIn](https://www.linkedin.com/in/aliaksandr-haiko-306674258/) · [GitHub](https://github.com/prxfsk17)