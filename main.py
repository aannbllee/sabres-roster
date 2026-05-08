from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select

from models import Player, engine, init_db

app = FastAPI()


@app.on_event("startup")
def startup() -> None:
    init_db()


@app.get("/player_stats")
def get_player_stats(player_name: str) -> dict[str, object] | dict[str, str]:
    with Session(engine) as session:
        statement = (
            select(Player)
            .where(Player.player_name == player_name)
        )
        result = session.exec(statement).first()

    if not result:
        return {"error": "Player not found"}

    return {
        "player_name": result.player_name,
        "jersey_number": result.jersey_number,
        "position": result.position,
        "height": result.height,
        "weight": result.weight,
        "birthplace": result.birthplace,
    }


@app.get("/players")
def get_players(
    position: str | None = None,
) -> list[dict[str, object]] | dict[str, str]:
    with Session(engine) as session:
        statement = select(Player)

        if position:
            statement = statement.where(Player.position == position)

        results = session.exec(statement).all()

    if not results:
        return {"error": "No players found"}

    return [
        {
            "player_name": result.player_name,
            "jersey_number": result.jersey_number,
            "position": result.position,
            "height": result.height,
            "weight": result.weight,
            "birthplace": result.birthplace,
        }
        for result in results
    ]


app.mount("/", StaticFiles(directory="static", html=True), name="static")