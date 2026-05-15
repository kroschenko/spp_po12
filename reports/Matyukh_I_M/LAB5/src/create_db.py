from database import SessionLocal, engine, Base
from models import Country, League, Team, Season, Match
from datetime import date


def init_database():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    england = Country(name="England", code="ENG", continent="Europe")
    spain = Country(name="Spain", code="ESP", continent="Europe")
    italy = Country(name="Italy", code="ITA", continent="Europe")
    germany = Country(name="Germany", code="GER", continent="Europe")
    france = Country(name="France", code="FRA", continent="Europe")

    db.add_all([england, spain, italy, germany, france])
    db.commit()

    premier_league = League(
        name="Premier League", country_id=england.id, level=1, founded_year=1992
    )
    la_liga = League(name="La Liga", country_id=spain.id, level=1, founded_year=1929)
    serie_a = League(name="Serie A", country_id=italy.id, level=1, founded_year=1898)
    bundesliga = League(
        name="Bundesliga", country_id=germany.id, level=1, founded_year=1963
    )
    ligue_1 = League(name="Ligue 1", country_id=france.id, level=1, founded_year=1930)

    db.add_all([premier_league, la_liga, serie_a, bundesliga, ligue_1])
    db.commit()

    teams_data = [
        (
            "Manchester United",
            "Manchester",
            england.id,
            premier_league.id,
            1878,
            "Old Trafford",
            74879,
        ),
        (
            "Liverpool",
            "Liverpool",
            england.id,
            premier_league.id,
            1892,
            "Anfield",
            53394,
        ),
        (
            "Arsenal",
            "London",
            england.id,
            premier_league.id,
            1886,
            "Emirates Stadium",
            60704,
        ),
        (
            "Chelsea",
            "London",
            england.id,
            premier_league.id,
            1905,
            "Stamford Bridge",
            40834,
        ),
        (
            "Manchester City",
            "Manchester",
            england.id,
            premier_league.id,
            1880,
            "Etihad Stadium",
            53400,
        ),
    ]

    teams = []
    for team_data in teams_data:
        team = Team(
            name=team_data[0],
            city=team_data[1],
            country_id=team_data[2],
            league_id=team_data[3],
            founded_year=team_data[4],
            stadium=team_data[5],
            capacity=team_data[6],
        )
        teams.append(team)

    db.add_all(teams)
    db.commit()

    season_2023 = Season(
        league_id=premier_league.id, year_start=2023, year_end=2024, number_of_teams=5
    )
    db.add(season_2023)
    db.commit()

    matches = [
        Match(
            season_id=season_2023.id,
            league_id=premier_league.id,
            home_team_id=teams[0].id,
            away_team_id=teams[1].id,
            match_date=date(2023, 8, 15),
            home_goals=2,
            away_goals=2,
            attendance=74000,
        ),
        Match(
            season_id=season_2023.id,
            league_id=premier_league.id,
            home_team_id=teams[2].id,
            away_team_id=teams[3].id,
            match_date=date(2023, 8, 16),
            home_goals=1,
            away_goals=0,
            attendance=60000,
        ),
        Match(
            season_id=season_2023.id,
            league_id=premier_league.id,
            home_team_id=teams[4].id,
            away_team_id=teams[0].id,
            match_date=date(2023, 8, 17),
            home_goals=3,
            away_goals=1,
            attendance=53000,
        ),
        Match(
            season_id=season_2023.id,
            league_id=premier_league.id,
            home_team_id=teams[1].id,
            away_team_id=teams[2].id,
            match_date=date(2023, 8, 22),
            home_goals=4,
            away_goals=0,
            attendance=53000,
        ),
    ]

    db.add_all(matches)
    db.commit()

    print("Database initialized successfully!")
    db.close()


if __name__ == "__main__":
    init_database()
