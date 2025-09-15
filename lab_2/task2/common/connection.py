from sqlmodel import SQLModel, create_engine, Session


DB_USERNAME = "entityfrm"
DB_PASSWORD = "pP3VJsoAcX2q"
DB_HOST = "ep-mute-sun-a2woi1rv-pooler.eu-central-1.aws.neon.tech"
DB_PORT = "5432"
DB_NAME = "web_dev_sem_6"

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL) # , echo=True


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine, expire_on_commit=True) as session:
        yield session
