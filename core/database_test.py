from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker,declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./docs/database.db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# for postgres or other relational databases
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver:5432/db"
# SQLALCHEMY_DATABASE_URL = "mysql://username:password@localhost/db_name"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False # only for sqlite
}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create base class for declaring tables
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30))
    last_name = Column(String(30), nullable=True)
    age = Column(Integer)
    
    @property
    def get_fullname(self):
        return f"{self.first_name} {self.last_name or ''}".strip()
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, fullname={self.get_fullname})"

# to create tables and database
Base.metadata.create_all(bind=engine)

# Create one database session.
session = SessionLocal()


try:
    # --------------------------------
    # Add one user
    # --------------------------------

    user = User(
        first_name="Ali Bigdeli",
        age=30
    )

    # Add the user to the current transaction.
    session.add(user)

    # Save the transaction to the database.
    session.commit()


    # --------------------------------
    # Add multiple users
    # --------------------------------

    users = [
        User(first_name="Maryam", age=26),
        User(first_name="Arousha", age=6)
    ]

    # Add multiple objects at once.
    session.add_all(users)

    # Save them to the database.
    session.commit()


    # --------------------------------
    # Read users
    # --------------------------------

    all_users = session.query(User).all()

    for user in all_users:
        print(user)


finally:
    # Always close the session when finished.
    session.close()