import smtplib
from datetime import datetime

import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

class Currencies:

    def __init__(self):
        load_dotenv()
        self.URL = os.getenv("SCRAPING_PAGE")
        self.usd_sorted = {}
        self.eur_sorted = {}

    def get_results(self, top_n=5):

        self.get_currencies()
        result = {
            "usd": dict(list(self.usd_sorted.items())[:top_n]),
            "eur": dict(list(self.eur_sorted.items())[:top_n]),
            "time": datetime.now().strftime('%d.%m.%Y')
        }
        return result

    def get_top(self, top_n=5):

        self.get_currencies()

        best_usd_bank = next(iter(self.usd_sorted)) if self.usd_sorted else None
        best_usd_rate = self.usd_sorted.get(best_usd_bank) if best_usd_bank else None

        best_eur_bank = next(iter(self.eur_sorted)) if self.eur_sorted else None
        best_eur_rate = self.eur_sorted.get(best_eur_bank) if best_eur_bank else None

        message_lines = [
            "=" * 50,
            "BEST CURRENCY RATES IN MINSK",
            "=" * 50,
            ""
        ]

        if best_usd_bank and best_usd_rate:
            message_lines.append(f"BEST US DOLLAR (USD) RATE:")
            message_lines.append(f"   {best_usd_bank}: {best_usd_rate} BYN")
            message_lines.append("")

        if best_eur_bank and best_eur_rate:
            message_lines.append(f"BEST EURO (EUR) RATE:")
            message_lines.append(f"   {best_eur_bank}: {best_eur_rate} BYN")
            message_lines.append("")

        message_lines.append("TOP-5 US DOLLAR (USD) RATES:")
        message_lines.append("-" * 30)

        if self.usd_sorted:
            for i, (bank, rate) in enumerate(list(self.usd_sorted.items())[:top_n], 1):
                prefix = ["1)", "2)", "3)", "4)", "5)"][i - 1]
                message_lines.append(f"{prefix} {bank}: {rate} BYN")

        message_lines.append("")

        message_lines.append("TOP-5 EURO (EUR) RATES:")
        message_lines.append("-" * 30)

        if self.eur_sorted:
            for i, (bank, rate) in enumerate(list(self.eur_sorted.items())[:top_n], 1):
                prefix = ["1)", "2)", "3)", "4)", "5)"][i - 1]
                message_lines.append(f"{prefix} {bank}: {rate} BYN")

        message_lines.append("")
        message_lines.append("=" * 50)
        message_lines.append("Updated: " + datetime.now().strftime("%d.%m.%Y %H:%M"))

        return "\n".join(message_lines)

    def get_currencies(self):

        page = requests.get(self.URL).text

        soup = BeautifulSoup(page, "html.parser")
        table = soup.find("tbody")
        banks = table.find_all(class_="currencies-courses__row-main")

        currencies_usd = {}
        currencies_eur = {}

        for bank in banks:
            parent_span = bank.select_one("td:first-child span img")
            name = parent_span.get("alt")
            currencies = bank.find_all("td")
            usd_currency = currencies[2]
            eur_currency = currencies[4]

            currencies_usd[name]=float(usd_currency.getText(strip=True))
            currencies_eur[name]=float(eur_currency.getText(strip=True))

        sorted_items = sorted(currencies_usd.items(), key=lambda item: item[1])
        self.usd_sorted = dict(sorted_items)
        sorted_items = sorted(currencies_eur.items(), key=lambda item: item[1])
        self.eur_sorted = dict(sorted_items)

    def send_email(self):

        message = self.get_top()

        sender_email = os.getenv("SENDER_MAIL")
        recipient_email = os.getenv("RECIPIENT_MAIL")
        password = os.getenv("PASSWORD_MAIL")

        subject = f"Currency Rates {datetime.now().strftime('%d.%m.%Y')}"
        email_content = f"Subject: {subject}\n\n{message}"

        email_bytes = email_content.encode('utf-8')

        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=sender_email, password=password)
            connection.sendmail(
                from_addr=sender_email,
                to_addrs=recipient_email,
                msg=email_bytes
        )