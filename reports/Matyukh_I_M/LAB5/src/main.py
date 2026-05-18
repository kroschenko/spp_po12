from fastapi import FastAPI, Depends, HTTPException
from typing import List, Optional

from database import get_db, engine, Base
from crud import *
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(title="European Football Championships API")


class CountryCreate(BaseModel):
    name: str
    code: str
    continent: str


class CountryResponse(BaseModel):
    id: int
    name: str
    code: str
    continent: str


class LeagueCreate(BaseModel):
    name: str
    country_id: int
    level: int
    founded_year: Optional[int] = None


class LeagueResponse(BaseModel):
    id: int
    name: str
    country_id: int
    level: int
    founded_year: Optional[int] = None


class TeamCreate(BaseModel):
    name: str
    city: str
    country_id: int
    league_id: Optional[int] = None
    founded_year: Optional[int] = None
    stadium: Optional[str] = None
    capacity: Optional[int] = None


class TeamResponse(BaseModel):
    id: int
    name: str
    city: str
    country_id: int
    league_id: Optional[int] = None
    founded_year: Optional[int] = None
    stadium: Optional[str] = None
    capacity: Optional[int] = None


class SeasonCreate(BaseModel):
    league_id: int
    year_start: int
    year_end: int
    number_of_teams: Optional[int] = None
    champion_team_id: Optional[int] = None


class SeasonResponse(BaseModel):
    id: int
    league_id: int
    year_start: int
    year_end: int
    number_of_teams: Optional[int] = None
    champion_team_id: Optional[int] = None


class MatchCreate(BaseModel):
    season_id: int
    league_id: int
    home_team_id: int
    away_team_id: int
    match_date: date
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    attendance: Optional[int] = None
    is_played: bool = True


class MatchResponse(BaseModel):
    id: int
    season_id: int
    league_id: int
    home_team_id: int
    away_team_id: int
    match_date: date
    home_goals: Optional[int] = None
    away_goals: Optional[int] = None
    attendance: Optional[int] = None
    is_played: bool


@app.post("/countries/", response_model=CountryResponse)
def create_country_endpoint(country: CountryCreate, db: Session = Depends(get_db)):
    return create_country(db, country.name, country.code, country.continent)


@app.get("/countries/", response_model=List[CountryResponse])
def read_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_countries(db, skip=skip, limit=limit)


@app.get("/countries/{country_id}", response_model=CountryResponse)
def read_country(country_id: int, db: Session = Depends(get_db)):
    db_country = get_country(db, country_id)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country


@app.put("/countries/{country_id}", response_model=CountryResponse)
def update_country_endpoint(
    country_id: int,
    name: str = None,
    code: str = None,
    continent: str = None,
    db: Session = Depends(get_db),
):
    db_country = update_country(db, country_id, name, code, continent)
    if db_country is None:
        raise HTTPException(status_code=404, detail="Country not found")
    return db_country


@app.delete("/countries/{country_id}")
def delete_country_endpoint(country_id: int, db: Session = Depends(get_db)):
    success = delete_country(db, country_id)
    if not success:
        raise HTTPException(status_code=404, detail="Country not found")
    return {"message": "Country deleted successfully"}


@app.post("/leagues/", response_model=LeagueResponse)
def create_league_endpoint(league: LeagueCreate, db: Session = Depends(get_db)):
    return create_league(
        db, league.name, league.country_id, league.level, league.founded_year
    )


@app.get("/leagues/", response_model=List[LeagueResponse])
def read_leagues(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_leagues(db, skip=skip, limit=limit)


@app.get("/leagues/{league_id}", response_model=LeagueResponse)
def read_league(league_id: int, db: Session = Depends(get_db)):
    db_league = get_league(db, league_id)
    if db_league is None:
        raise HTTPException(status_code=404, detail="League not found")
    return db_league


@app.put("/leagues/{league_id}", response_model=LeagueResponse)
def update_league_endpoint(
    league_id: int,
    name: str = None,
    level: int = None,
    founded_year: int = None,
    db: Session = Depends(get_db),
):
    db_league = update_league(
        db, league_id, name=name, level=level, founded_year=founded_year
    )
    if db_league is None:
        raise HTTPException(status_code=404, detail="League not found")
    return db_league


@app.delete("/leagues/{league_id}")
def delete_league_endpoint(league_id: int, db: Session = Depends(get_db)):
    success = delete_league(db, league_id)
    if not success:
        raise HTTPException(status_code=404, detail="League not found")
    return {"message": "League deleted successfully"}


@app.post("/teams/", response_model=TeamResponse)
def create_team_endpoint(team: TeamCreate, db: Session = Depends(get_db)):
    return create_team(
        db,
        team.name,
        team.city,
        team.country_id,
        team.league_id,
        team.founded_year,
        team.stadium,
        team.capacity,
    )


@app.get("/teams/", response_model=List[TeamResponse])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_teams(db, skip=skip, limit=limit)


@app.get("/teams/{team_id}", response_model=TeamResponse)
def read_team(team_id: int, db: Session = Depends(get_db)):
    db_team = get_team(db, team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@app.put("/teams/{team_id}", response_model=TeamResponse)
def update_team_endpoint(
    team_id: int,
    name: str = None,
    city: str = None,
    stadium: str = None,
    capacity: int = None,
    db: Session = Depends(get_db),
):
    db_team = update_team(
        db, team_id, name=name, city=city, stadium=stadium, capacity=capacity
    )
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team


@app.delete("/teams/{team_id}")
def delete_team_endpoint(team_id: int, db: Session = Depends(get_db)):
    success = delete_team(db, team_id)
    if not success:
        raise HTTPException(status_code=404, detail="Team not found")
    return {"message": "Team deleted successfully"}


@app.post("/seasons/", response_model=SeasonResponse)
def create_season_endpoint(season: SeasonCreate, db: Session = Depends(get_db)):
    return create_season(
        db,
        season.league_id,
        season.year_start,
        season.year_end,
        season.number_of_teams,
        season.champion_team_id,
    )


@app.get("/seasons/", response_model=List[SeasonResponse])
def read_seasons(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_seasons(db, skip=skip, limit=limit)


@app.get("/seasons/{season_id}", response_model=SeasonResponse)
def read_season(season_id: int, db: Session = Depends(get_db)):
    db_season = get_season(db, season_id)
    if db_season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return db_season


@app.put("/seasons/{season_id}", response_model=SeasonResponse)
def update_season_endpoint(
    season_id: int,
    champion_team_id: int = None,
    number_of_teams: int = None,
    db: Session = Depends(get_db),
):
    db_season = update_season(
        db,
        season_id,
        champion_team_id=champion_team_id,
        number_of_teams=number_of_teams,
    )
    if db_season is None:
        raise HTTPException(status_code=404, detail="Season not found")
    return db_season


@app.delete("/seasons/{season_id}")
def delete_season_endpoint(season_id: int, db: Session = Depends(get_db)):
    success = delete_season(db, season_id)
    if not success:
        raise HTTPException(status_code=404, detail="Season not found")
    return {"message": "Season deleted successfully"}


@app.post("/matches/", response_model=MatchResponse)
def create_match_endpoint(match: MatchCreate, db: Session = Depends(get_db)):
    return create_match(
        db,
        match.season_id,
        match.league_id,
        match.home_team_id,
        match.away_team_id,
        match.match_date,
        match.home_goals,
        match.away_goals,
        match.attendance,
    )


@app.get("/matches/", response_model=List[MatchResponse])
def read_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_matches(db, skip=skip, limit=limit)


@app.get("/matches/{match_id}", response_model=MatchResponse)
def read_match(match_id: int, db: Session = Depends(get_db)):
    db_match = get_match(db, match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@app.put("/matches/{match_id}", response_model=MatchResponse)
def update_match_endpoint(
    match_id: int,
    home_goals: int = None,
    away_goals: int = None,
    attendance: int = None,
    is_played: bool = None,
    db: Session = Depends(get_db),
):
    db_match = update_match(
        db,
        match_id,
        home_goals=home_goals,
        away_goals=away_goals,
        attendance=attendance,
        is_played=is_played,
    )
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match


@app.delete("/matches/{match_id}")
def delete_match_endpoint(match_id: int, db: Session = Depends(get_db)):
    success = delete_match(db, match_id)
    if not success:
        raise HTTPException(status_code=404, detail="Match not found")
    return {"message": "Match deleted successfully"}


@app.get("/league-table/{season_id}")
def get_league_table_endpoint(season_id: int, db: Session = Depends(get_db)):
    table = get_league_table(db, season_id)
    # Add team names to the table
    for entry in table:
        team = get_team(db, entry["team_id"])
        entry["team_name"] = team.name if team else "Unknown"
    return table


@app.get("/")
def root():
    return {
        "message": "European Football Championships API",
        "docs": "http://127.0.0.1:8000/docs",
        "endpoints": {
            "countries": "/countries/",
            "leagues": "/leagues/",
            "teams": "/teams/",
            "seasons": "/seasons/",
            "matches": "/matches/",
            "league_table": "/league-table/{season_id}",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
