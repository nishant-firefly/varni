import os
from alembic.config import Config
from alembic import command
from . import copy_bootstrap  # Assuming copy_bootstrap is in the same module

class MigrationManager:
    def __init__(self, alembic_config_path="alembic.ini", db_url=None):
        self.alembic_cfg = self.get_alembic_config(alembic_config_path, db_url)
        self.target_metadata = None

    def get_alembic_config(self, alembic_path, db_url):
        config = Config(alembic_path)

        if db_url:
            config.set_main_option('sqlalchemy.url', db_url)
        
        return config

    def setup_metadata(self, models_module):
        # Dynamically import the models module and set up metadata
        models = __import__(models_module, fromlist=['Base'])
        self.target_metadata = models.Base.metadata

    def makemigrations(self, message="Auto migration"):
        """Generate migration files from model changes."""
        command.revision(self.alembic_cfg, autogenerate=True, message=message)

    def migrate(self):
        """Apply migrations to the database."""
        command.upgrade(self.alembic_cfg, "head")

    def rollback(self, steps=1):
        """Roll back the last migration(s)."""
        command.downgrade(self.alembic_cfg, f"-{steps}")

    def history(self):
        """Show migration history."""
        command.history(self.alembic_cfg)

    def setup_database(self, bootstrap_destination=None, alembic_config_path=None, db_url=None, models_module="models"):
        """
        Set up the database by copying the bootstrap folder, applying migrations, and configuring the database.

        :param bootstrap_destination: The directory where the bootstrap files should be copied.
        :param alembic_config_path: Path to the alembic.ini file (if not provided, it will use the default).
        :param db_url: The database connection string.
        :param models_module: The Python module path to the SQLAlchemy models.
        """
        if bootstrap_destination:
            copy_bootstrap(bootstrap_destination)
            alembic_config_path = os.path.join(bootstrap_destination, 'alembic.ini')
        
        # Run migrations
        run_migrations(alembic_config_path=alembic_config_path, db_url=db_url, models_module=models_module)
        print("Database setup completed with migrations.")

def run_makemigrations(alembic_config_path="alembic.ini", db_url=None, models_module="models", message="Auto migration"):
    """Generate a new migration file based on changes in the models."""
    migration_manager = MigrationManager(alembic_config_path=alembic_config_path, db_url=db_url)
    migration_manager.setup_metadata(models_module)
    migration_manager.makemigrations(message)

def run_migrate(alembic_config_path="alembic.ini", db_url=None, models_module="models"):
    """Apply migrations to the database."""
    migration_manager = MigrationManager(alembic_config_path=alembic_config_path, db_url=db_url)
    migration_manager.setup_metadata(models_module)
    migration_manager.migrate()

def run_migrations(alembic_config_path="alembic.ini", db_url=None, models_module="models"):
    """Run both makemigrations and migrate sequentially."""
    run_makemigrations(alembic_config_path, db_url, models_module)
    run_migrate(alembic_config_path, db_url, models_module)
