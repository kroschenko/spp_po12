from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from database import Base


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    code = Column(String(3), nullable=False, unique=True)
    continent = Column(String(50), nullable=False)

    leagues = relationship("League", back_populates="country")
    teams = relationship("Team", back_populates="country")


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    level = Column(Integer, nullable=False)
    founded_year = Column(Integer)
    is_professional = Column(Boolean, default=True)

    country = relationship("Country", back_populates="leagues")
    teams = relationship("Team", back_populates="league")
    matches = relationship("Match", back_populates="league")
    seasons = relationship("Season", back_populates="league")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100))
    founded_year = Column(Integer)
    stadium = Column(String(200))
    capacity = Column(Integer)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"))

    country = relationship("Country", back_populates="teams")
    league = relationship("League", back_populates="teams")
    home_matches = relationship(
        "Match", foreign_keys="Match.home_team_id", back_populates="home_team"
    )
    away_matches = relationship(
        "Match", foreign_keys="Match.away_team_id", back_populates="away_team"
    )


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    year_start = Column(Integer, nullable=False)
    year_end = Column(Integer, nullable=False)
    number_of_teams = Column(Integer)
    champion_team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)

    league = relationship("League", back_populates="seasons")
    champion = relationship("Team", foreign_keys=[champion_team_id])
    matches = relationship("Match", back_populates="season")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), nullable=False)
    league_id = Column(Integer, ForeignKey("leagues.id"), nullable=False)
    home_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    away_team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    match_date = Column(Date, nullable=False)
    home_goals = Column(Integer)
    away_goals = Column(Integer)
    attendance = Column(Integer)
    is_played = Column(Boolean, default=True)

    season = relationship("Season", back_populates="matches")
    league = relationship("League", back_populates="matches")
    home_team = relationship("Team", foreign_keys=[home_team_id])
    away_team = relationship("Team", foreign_keys=[away_team_id])
