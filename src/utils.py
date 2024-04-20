from fastapi import  Query
import json

class MatchesQueryParams:
    def __init__(
        self,
        date_init: str = Query(..., description="Date init query (yyyy-mm-dd)"),
        date_end: str = Query(..., description="Date end query (yyyy-mm-dd)"),
        goals: int = Query(0, description="Goals in match"),
    ):
        self.date_init = date_init
        self.date_end = date_end
        self.goals = goals

class ListQueryParams:
    def __init__(
        self,
        team_name : str = Query(None, description="Query team name (Liverpool, Manchester...)"),
        page: int = Query(1, description="Page"),
    ):
        self.team_name = team_name
        self.page = page

mock_matches = json.loads("""
        {
    "filters": {
        "dateFrom": "2024-03-15",
        "dateTo": "2024-03-25",
        "permission": "TIER_ONE",
        "status": [
            "FINISHED"
        ],
        "competitions": "PL"
    },
    "resultSet": {
        "count": 4,
        "competitions": "PL",
        "first": "2024-03-16",
        "last": "2024-03-17",
        "played": 4
    },
    "matches": [
        {
            "area": {
                "id": 2072,
                "name": "England",
                "code": "ENG",
                "flag": "https://crests.football-data.org/770.svg"
            },
            "competition": {
                "id": 2021,
                "name": "Premier League",
                "code": "PL",
                "type": "LEAGUE",
                "emblem": "https://crests.football-data.org/PL.png"
            },
            "season": {
                "id": 1564,
                "startDate": "2023-08-11",
                "endDate": "2024-05-19",
                "currentMatchday": 34,
                "winner": null
            },
            "id": 436229,
            "utcDate": "2024-03-16T15:00:00Z",
            "status": "FINISHED",
            "matchday": 29,
            "stage": "REGULAR_SEASON",
            "group": null,
            "lastUpdated": "2024-03-17T05:21:23Z",
            "homeTeam": {
                "id": 389,
                "name": "Luton Town FC",
                "shortName": "Luton Town",
                "tla": "LUT",
                "crest": "https://crests.football-data.org/389.png"
            },
            "awayTeam": {
                "id": 351,
                "name": "Nottingham Forest FC",
                "shortName": "Nottingham",
                "tla": "NOT",
                "crest": "https://crests.football-data.org/351.png"
            },
            "score": {
                "winner": "DRAW",
                "duration": "REGULAR",
                "fullTime": {
                    "home": 1,
                    "away": 1
                },
                "halfTime": {
                    "home": 0,
                    "away": 1
                }
            },
            "odds": {
                "msg": "Activate Odds-Package in User-Panel to retrieve odds."
            },
            "referees": [
                {
                    "id": 11469,
                    "name": "Darren England",
                    "type": "REFEREE",
                    "nationality": "England"
                }
            ]
        },
        {
            "area": {
                "id": 2072,
                "name": "England",
                "code": "ENG",
                "flag": "https://crests.football-data.org/770.svg"
            },
            "competition": {
                "id": 2021,
                "name": "Premier League",
                "code": "PL",
                "type": "LEAGUE",
                "emblem": "https://crests.football-data.org/PL.png"
            },
            "season": {
                "id": 1564,
                "startDate": "2023-08-11",
                "endDate": "2024-05-19",
                "currentMatchday": 34,
                "winner": null
            },
            "id": 436225,
            "utcDate": "2024-03-16T15:00:00Z",
            "status": "FINISHED",
            "matchday": 29,
            "stage": "REGULAR_SEASON",
            "group": null,
            "lastUpdated": "2024-03-17T05:21:23Z",
            "homeTeam": {
                "id": 328,
                "name": "Burnley FC",
                "shortName": "Burnley",
                "tla": "BUR",
                "crest": "https://crests.football-data.org/328.png"
            },
            "awayTeam": {
                "id": 402,
                "name": "Brentford FC",
                "shortName": "Brentford",
                "tla": "BRE",
                "crest": "https://crests.football-data.org/402.png"
            },
            "score": {
                "winner": "HOME_TEAM",
                "duration": "REGULAR",
                "fullTime": {
                    "home": 2,
                    "away": 1
                },
                "halfTime": {
                    "home": 1,
                    "away": 0
                }
            },
            "odds": {
                "msg": "Activate Odds-Package in User-Panel to retrieve odds."
            },
            "referees": [
                {
                    "id": 11317,
                    "name": "Darren Bond",
                    "type": "REFEREE",
                    "nationality": "England"
                }
            ]
        },
        {
            "area": {
                "id": 2072,
                "name": "England",
                "code": "ENG",
                "flag": "https://crests.football-data.org/770.svg"
            },
            "competition": {
                "id": 2021,
                "name": "Premier League",
                "code": "PL",
                "type": "LEAGUE",
                "emblem": "https://crests.football-data.org/PL.png"
            },
            "season": {
                "id": 1564,
                "startDate": "2023-08-11",
                "endDate": "2024-05-19",
                "currentMatchday": 34,
                "winner": null
            },
            "id": 436228,
            "utcDate": "2024-03-16T17:30:00Z",
            "status": "FINISHED",
            "matchday": 29,
            "stage": "REGULAR_SEASON",
            "group": null,
            "lastUpdated": "2024-03-17T05:21:23Z",
            "homeTeam": {
                "id": 63,
                "name": "Fulham FC",
                "shortName": "Fulham",
                "tla": "FUL",
                "crest": "https://crests.football-data.org/63.svg"
            },
            "awayTeam": {
                "id": 73,
                "name": "Tottenham Hotspur FC",
                "shortName": "Tottenham",
                "tla": "TOT",
                "crest": "https://crests.football-data.org/73.svg"
            },
            "score": {
                "winner": "HOME_TEAM",
                "duration": "REGULAR",
                "fullTime": {
                    "home": 3,
                    "away": 0
                },
                "halfTime": {
                    "home": 1,
                    "away": 0
                }
            },
            "odds": {
                "msg": "Activate Odds-Package in User-Panel to retrieve odds."
            },
            "referees": [
                {
                    "id": 11446,
                    "name": "Robert Jones",
                    "type": "REFEREE",
                    "nationality": "England"
                }
            ]
        },
        {
            "area": {
                "id": 2072,
                "name": "England",
                "code": "ENG",
                "flag": "https://crests.football-data.org/770.svg"
            },
            "competition": {
                "id": 2021,
                "name": "Premier League",
                "code": "PL",
                "type": "LEAGUE",
                "emblem": "https://crests.football-data.org/PL.png"
            },
            "season": {
                "id": 1564,
                "startDate": "2023-08-11",
                "endDate": "2024-05-19",
                "currentMatchday": 34,
                "winner": null
            },
            "id": 436231,
            "utcDate": "2024-03-17T14:00:00Z",
            "status": "FINISHED",
            "matchday": 29,
            "stage": "REGULAR_SEASON",
            "group": null,
            "lastUpdated": "2024-03-17T20:21:07Z",
            "homeTeam": {
                "id": 563,
                "name": "West Ham United FC",
                "shortName": "West Ham",
                "tla": "WHU",
                "crest": "https://crests.football-data.org/563.png"
            },
            "awayTeam": {
                "id": 58,
                "name": "Aston Villa FC",
                "shortName": "Aston Villa",
                "tla": "AVL",
                "crest": "https://crests.football-data.org/58.png"
            },
            "score": {
                "winner": "DRAW",
                "duration": "REGULAR",
                "fullTime": {
                    "home": 1,
                    "away": 1
                },
                "halfTime": {
                    "home": 1,
                    "away": 0
                }
            },
            "odds": {
                "msg": "Activate Odds-Package in User-Panel to retrieve odds."
            },
            "referees": [
                {
                    "id": 23568,
                    "name": "Jarred Gillett",
                    "type": "REFEREE",
                    "nationality": "Australia"
                }
            ]
        }
    ]
} """)