from api.models import Base, engine

def init_db():
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    print("Database schema created successfully.")

if __name__ == "__main__":
    init_db()
