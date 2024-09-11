# File: varni/dbs/migrations/manage_migrations.py
import argparse
import os
from migration_manager import MigrationManager

def main():
    parser = argparse.ArgumentParser(description="Manage database migrations and setup using Alembic.")
    parser.add_argument('command', choices=['new-db-setup', 'update-db', 'push-db', 'seed-db', 'apply-sql'], help="Commands: 'new-db-setup' to initialize the project, 'update-db' to generate and apply model changes, 'push-db' to apply migrations, 'seed-db' to insert initial data, 'apply-sql' to apply a SQL patch.")
    parser.add_argument('--sql-file', help="Path to the SQL file for the 'apply-sql' command.")
    args = parser.parse_args()

    migration_manager = MigrationManager()

    if args.command == 'new-db-setup':
        print(f"Setting up new project: {os.getenv('PROJECT_NAME')}")
        migration_manager.run_migrations()
        migration_manager.seed_data()
    elif args.command == 'update-db':
        print("Updating the database with new migrations...")
        migration_manager.makemigrations()
    elif args.command == 'push-db':
        print("Pushing the latest migrations to the database...")
        migration_manager.migrate()
    elif args.command == 'seed-db':
        print("Seeding initial data into the database...")
        migration_manager.seed_data()
    elif args.command == 'apply-sql':
        if args.sql_file:
            print(f"Applying SQL patch: {args.sql_file}")
            migration_manager.apply_sql_patch(args.sql_file)
        else:
            print("Please provide a SQL file path with the --sql-file argument.")

if __name__ == "__main__":
    main()
