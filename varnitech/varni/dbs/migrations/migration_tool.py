import argparse
from varni.dbs.migrations.migration_manager import MigrationManager

def main():
    parser = argparse.ArgumentParser(description="Manage database migrations and setup using Alembic.")
    parser.add_argument('command', choices=['init', 'migrate', 'update', 'apply'], help="Commands: 'init' for initial setup, 'migrate' to create a new migration, 'update' to apply migrations, 'apply' to run all migrations.")
    args = parser.parse_args()

    migration_manager = MigrationManager()

    if args.command == 'init':
        print("Initializing database...")
        migration_manager.run_migrations()
    elif args.command == 'migrate':
        print("Creating new migration...")
        migration_manager.makemigrations()
    elif args.command == 'update':
        print("Applying latest migrations...")
        migration_manager.migrate()
    elif args.command == 'apply':
        print("Running all migrations...")
        migration_manager.run_migrations()

if __name__ == "__main__":
    main()
