def get_test_circuits():
    return [{
        'id': 1,
        'name': 'Albert Park Circuit',
        'image': 'https://media.api-sports.io/formula-1/circuits/1.png',
        'competition': {
            'id': 1,
            'name': 'Australia Grand Prix',
            'location': {'country': 'Australia', 'city': 'Melbourne'}
        },
        'first_grand_prix': 1996,
        'laps': 58,
        'length': '5.278 km',
        'race_distance': '306.124 km',
        'lap_record': {
            'time': '1:19.813',
            'driver': 'Charles Leclerc',
            'year': '2024'
        },
        'capacity': 80000,
        'opened': 1953,
        'owner': None
    }]


def get_test_teams():
    return [
        {
            "id": 1,
            "name": "Red Bull Racing",
            "logo": "https://media.api-sports.io/formula-1/teams/1.png",
            "base": "Milton Keynes, United Kingdom",
            "first_team_entry": 1997,
            "world_championships": 4,
            "highest_race_finish": {
                "position": 1,
                "number": 75
            },
            "pole_positions": 73,
            "fastest_laps": 76,
            "president": "Dietrich Mateschitz",
            "director": "Christian Horner",
            "technical_manager": "Pierre Waché",
            "chassis": "RB18",
            "engine": "Red Bull Powertrains",
            "tyres": "Pirelli"
        }
    ]

def get_test_drivers():
    return [
        {
            "id": 20,
            "name": "Lewis Hamilton",
            "abbr": "HAM",
            "image": "https://media.api-sports.io/formula-1/drivers/20.png",
            "nationality": "British",
            "country": {
                "name": "United Kingdom",
                "code": "GB"
            },
            "birthdate": "1985-01-07",
            "birthplace": "Stevenage, England",
            "number": 44,
            "grands_prix_entered": 288,
            "world_championships": 7,
            "podiums": 182,
            "highest_race_finish": {
                "position": 1,
                "number": 103
            },
            "highest_grid_position": 1,
            "career_points": "4165.5",
            "teams": [
                {
                    "season": 2022,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2021,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2020,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2019,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2018,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2017,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2016,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2015,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2014,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2013,
                    "team": {
                        "id": 5,
                        "name": "Mercedes-AMG Petronas",
                        "logo": "https://media.api-sports.io/formula-1/teams/5.png"
                    }
                },
                {
                    "season": 2012,
                    "team": {
                        "id": 2,
                        "name": "McLaren Racing",
                        "logo": "https://media.api-sports.io/formula-1/teams/2.png"
                    }
                },
                {
                    "season": 2011,
                    "team": {
                        "id": 2,
                        "name": "McLaren Racing",
                        "logo": "https://media.api-sports.io/formula-1/teams/2.png"
                    }
                }
            ]
        }
    ]
