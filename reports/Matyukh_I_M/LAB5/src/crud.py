from sqlalchemy.orm import Session
from models import Country, League, Team, Season, Match
from datetime import date


def create_country(db: Session, name: str, code: str, continent: str):
    country = Country(name=name, code=code, continent=continent)
    db.add(country)
    db.commit()
    db.refresh(country)
    return country


def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Country).offset(skip).limit(limit).all()


def get_country(db: Session, country_id: int):
    return db.query(Country).filter(Country.id == country_id).first()


def update_country(
    db: Session,
    country_id: int,
    name: str = None,
    code: str = None,
    continent: str = None,
):
    country = get_country(db, country_id)
    if country:
        if name:
            country.name = name
        if code:
            country.code = code
        if continent:
            country.continent = continent
        db.commit()
        db.refresh(country)
    return country


def delete_country(db: Session, country_id: int):
    country = get_country(db, country_id)
    if country:
        db.delete(country)
        db.commit()
        return True
    return False


def create_league(
    db: Session, name: str, country_id: int, level: int, founded_year: int = None
):
    league = League(
        name=name, country_id=country_id, level=level, founded_year=founded_year
    )
    db.add(league)
    db.commit()
    db.refresh(league)
    return league


def get_leagues(db: Session, skip: int = 0, limit: int = 100):
    return db.query(League).offset(skip).limit(limit).all()


def get_league(db: Session, league_id: int):
    return db.query(League).filter(League.id == league_id).first()


def update_league(db: Session, league_id: int, **kwargs):
    league = get_league(db, league_id)
    if league:
        for key, value in kwargs.items():
            if hasattr(league, key) and value is not None:
                setattr(league, key, value)
        db.commit()
        db.refresh(league)
    return league


def delete_league(db: Session, league_id: int):
    league = get_league(db, league_id)
    if league:
        db.delete(league)
        db.commit()
        return True
    return False


def create_team(
    db: Session,
    name: str,
    city: str,
    country_id: int,
    league_id: int = None,
    founded_year: int = None,
    stadium: str = None,
    capacity: int = None,
):
    team = Team(
        name=name,
        city=city,
        country_id=country_id,
        league_id=league_id,
        founded_year=founded_year,
        stadium=stadium,
        capacity=capacity,
    )
    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Team).offset(skip).limit(limit).all()


def get_team(db: Session, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()


def update_team(db: Session, team_id: int, **kwargs):
    team = get_team(db, team_id)
    if team:
        for key, value in kwargs.items():
            if hasattr(team, key) and value is not None:
                setattr(team, key, value)
        db.commit()
        db.refresh(team)
    return team


def delete_team(db: Session, team_id: int):
    team = get_team(db, team_id)
    if team:
        db.delete(team)
        db.commit()
        return True
    return False


def create_season(
    db: Session,
    league_id: int,
    year_start: int,
    year_end: int,
    number_of_teams: int = None,
    champion_team_id: int = None,
):
    season = Season(
        league_id=league_id,
        year_start=year_start,
        year_end=year_end,
        number_of_teams=number_of_teams,
        champion_team_id=champion_team_id,
    )
    db.add(season)
    db.commit()
    db.refresh(season)
    return season


def get_seasons(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Season).offset(skip).limit(limit).all()


def get_season(db: Session, season_id: int):
    return db.query(Season).filter(Season.id == season_id).first()


def update_season(db: Session, season_id: int, **kwargs):
    season = get_season(db, season_id)
    if season:
        for key, value in kwargs.items():
            if hasattr(season, key) and value is not None:
                setattr(season, key, value)
        db.commit()
        db.refresh(season)
    return season


def delete_season(db: Session, season_id: int):
    season = get_season(db, season_id)
    if season:
        db.delete(season)
        db.commit()
        return True
    return False


def create_match(
    db: Session,
    season_id: int,
    league_id: int,
    home_team_id: int,
    away_team_id: int,
    match_date: date,
    home_goals: int = None,
    away_goals: int = None,
    attendance: int = None,
):
    match = Match(
        season_id=season_id,
        league_id=league_id,
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        match_date=match_date,
        home_goals=home_goals,
        away_goals=away_goals,
        attendance=attendance,
    )
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Match).offset(skip).limit(limit).all()


def get_match(db: Session, match_id: int):
    return db.query(Match).filter(Match.id == match_id).first()


def update_match(db: Session, match_id: int, **kwargs):
    match = get_match(db, match_id)
    if match:
        for key, value in kwargs.items():
            if hasattr(match, key) and value is not None:
                setattr(match, key, value)
        db.commit()
        db.refresh(match)
    return match


def delete_match(db: Session, match_id: int):
    match = get_match(db, match_id)
    if match:
        db.delete(match)
        db.commit()
        return True
    return False


def get_league_table(db: Session, season_id: int):
    """Get league table for a specific season"""
    matches = (
        db.query(Match)
        .filter(Match.season_id == season_id, Match.is_played == True)
        .all()
    )

    table = {}
    for match in matches:
        # Home team
        if match.home_team_id not in table:
            table[match.home_team_id] = {
                "team_id": match.home_team_id,
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "gf": 0,
                "ga": 0,
                "points": 0,
            }

        if match.away_team_id not in table:
            table[match.away_team_id] = {
                "team_id": match.away_team_id,
                "played": 0,
                "won": 0,
                "drawn": 0,
                "lost": 0,
                "gf": 0,
                "ga": 0,
                "points": 0,
            }

        table[match.home_team_id]["played"] += 1
        table[match.home_team_id]["gf"] += match.home_goals
        table[match.home_team_id]["ga"] += match.away_goals

        table[match.away_team_id]["played"] += 1
        table[match.away_team_id]["gf"] += match.away_goals
        table[match.away_team_id]["ga"] += match.home_goals

        if match.home_goals > match.away_goals:
            table[match.home_team_id]["won"] += 1
            table[match.home_team_id]["points"] += 3
            table[match.away_team_id]["lost"] += 1
        elif match.home_goals < match.away_goals:
            table[match.away_team_id]["won"] += 1
            table[match.away_team_id]["points"] += 3
            table[match.home_team_id]["lost"] += 1
        else:
            table[match.home_team_id]["drawn"] += 1
            table[match.away_team_id]["drawn"] += 1
            table[match.home_team_id]["points"] += 1
            table[match.away_team_id]["points"] += 1

    return sorted(table.values(), key=lambda x: (-x["points"], x["gd"]))
