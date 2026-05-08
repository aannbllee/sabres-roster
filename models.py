from sqlmodel import SQLModel, Field, Session, create_engine
from sqlalchemy import text


class Player(SQLModel, table=True):
    player_name: str = Field(primary_key=True)
    jersey_number: int | None = None
    position: str
    shoots: str | None = None
    height: str | None = None
    weight: int | None = None
    birth_date: str | None = None
    birthplace: str | None = None


engine = create_engine("sqlite:///nhl.db", echo=False)


def init_db():
    """Create all database tables."""

    # Optional lightweight migration if schema changes later
    with Session(engine) as session:
        table_exists = session.exec(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='player'")
        ).first()

        if table_exists:
            columns = session.exec(text("PRAGMA table_info(player)")).all()
            column_names = {str(col[1]) for col in columns}

            expected_columns = {
                "player_name",
                "jersey_number",
                "position",
                "shoots",
                "height",
                "weight",
                "birth_date",
                "birthplace",
            }

            # If schema changes, rebuild table
            if not expected_columns.issubset(column_names):
                session.exec(text("DROP TABLE player"))
                session.commit()

    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Tables created.")