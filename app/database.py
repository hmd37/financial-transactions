from sqlmodel import Session, create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:12345@db:5432/finance"
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
