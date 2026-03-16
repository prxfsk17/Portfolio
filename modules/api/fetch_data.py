import requests
from modules.api.test_data import get_test_circuits, get_test_teams, get_test_drivers
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("F1_KEY")
API_URL_CIRCUITS = os.getenv("F1_URL_CIRC")
API_URL_TEAMS = os.getenv("F1_URL_TEAMS")
API_URL_DRIVERS = os.getenv("F1_URL_DRIVERS")

def safe_get_capacity(capacity):
    if capacity is None:
        return 0
    elif isinstance(capacity, int):
        return capacity
    elif isinstance(capacity, str):
        try:
            return int(capacity.replace(',', '').replace('.', '').replace(' ', ''))
        except (ValueError, AttributeError):
            return 0
    else:
        return 0

def get_headers():
    return {'x-apisports-key': API_KEY}

def fetch_circuits_from_api():
    try:
        response = requests.get(API_URL_CIRCUITS, headers=get_headers(), timeout=10)
        response.raise_for_status()
        data = response.json()
        circuits = data.get("response", [])

        if circuits:
            for circuit in circuits:
                capacity = circuit.get('capacity')
                circuit['capacity'] = safe_get_capacity(capacity)
            return circuits
        else:
            return get_test_circuits()

    except requests.exceptions.RequestException as e:
        print(e)
        return get_test_circuits()
    except Exception as e:
        print(e)
        return get_test_circuits()


def fetch_teams_from_api():
    try:
        response = requests.get(API_URL_TEAMS, headers=get_headers(), timeout=10)
        response.raise_for_status()
        data = response.json()
        teams = data.get("response", [])

        if teams:
            return teams
        else:
            return get_test_teams()

    except requests.exceptions.RequestException as e:
        print(e)
        return get_test_teams()
    except Exception as e:
        print(e)
        return get_test_teams()


def fetch_drivers_from_api(search):
    try:
        parameters={
            "search":search
        }
        response = requests.get(API_URL_DRIVERS, headers=get_headers(), params=parameters, timeout=10)
        response.raise_for_status()
        data = response.json()
        drivers = data.get("response", [])
        if drivers:
            return drivers
        else:
            return []

    except requests.exceptions.RequestException as e:
        print(e)
        return get_test_drivers()
    except Exception as e:
        print(e)
        return get_test_drivers()
