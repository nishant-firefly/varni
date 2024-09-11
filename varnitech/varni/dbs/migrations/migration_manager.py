import os
from alembic import command
from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from varni.dbs.auth.models import Base as AuthBase

class MigrationManager:
    def __init__(self):
        self.alembic_cfg = Config("alembic.ini")

    def setup_metadata(self):
        # Add all models' Base classes here
        from example_project.models.custom_user import Base as CustomUserBase
        self.target_metadata = [AuthBase.metadata, CustomUserBase.metadata]

    def makemigrations(self):
        """Create a new migration based on model changes."""
        self.setup_metadata()

        script_directory = self.alembic_cfg.get_main_option("script_location")
        script = command.ScriptDirectory(script_directory)

        if script.get_current_head():
            engine = create_engine(self.alembic_cfg.get_main_option("sqlalchemy.url"))
            with engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_rev = context.get_current_revision()

                if current_rev:
                    print(f"Creating migration for revision {current_rev}")
                else:
                    print("No changes detected. No new migration file created.")
        else:
            print("No previous migrations found. You must create an initial migration first.")

        command.revision(self.alembic_cfg, autogenerate=True, message="Auto migration based on model changes.")

    def migrate(self):
        """Apply the migrations to the database."""
        command.upgrade(self.alembic_cfg, "head")

    def rollback(self):
        """Roll back the last migration."""
        command.downgrade(self.alembic_cfg, "-1")

    def seed_data(self):
        """Seed the database with initial data."""
        engine = create_engine(self.alembic_cfg.get_main_option("sqlalchemy.url"))
        Session = sessionmaker(bind=engine)
        session = Session()

        # Example seeding logic
        from example_project.models.custom_user import CustomUser
        user = CustomUser(username="admin", password="admin")
        session.add(user)
        session.commit()
        print("Database seeded with initial data.")
