import csv
from pathlib import Path
from sqlmodel import Session, delete
from models import Player, engine, init_db

def populate_db():
    """Populate the database with player data from CSV."""
    init_db()

    csv_path = Path(__file__).with_name("sabres_roster.csv")

    # Parse CSV first so we never wipe existing rows if parsing fails.
    with csv_path.open("r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        players: list[Player] = []

        for row in reader:
            players.append(
                Player(
                    player_name=row["player_name"],
                    jersey_number=int(row["jersey_number"]) if row["jersey_number"] else None,
                    position=row["position"],
                    shoots=row["shoots"],
                    height=row["height"],
                    weight=int(row["weight"]) if row["weight"] else None,
                )
            )

    # Replace player rows only
    with Session(engine) as session:
        session.exec(delete(Player))

        for player in players:
            session.add(player)

        session.commit()

    print(f"Successfully inserted {len(players)} players into the database!")


if __name__ == "__main__":
    populate_db()