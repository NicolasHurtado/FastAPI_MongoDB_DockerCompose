from fastapi import  Query

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
