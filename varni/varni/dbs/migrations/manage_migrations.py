import argparse
from migrate_tool import run_makemigrations, run_migrate, run_migrations

def main():
    parser = argparse.ArgumentParser(description="Manage database migrations using Alembic.")
    
    parser.add_argument(
        'command', 
        choices=['makemigrations', 'migrate', 'migrations'], 
        help="Command to run: 'makemigrations' to generate migration files, 'migrate' to apply migrations, 'migrations' to run both sequentially."
    )

    parser.add_argument(
        '--alembic-config', 
        default='alembic.ini', 
        help="Path to the Alembic configuration file. Default is 'alembic.ini' in the current directory."
    )

    parser.add_argument(
        '--db-url', 
        required=True, 
        help="Database URL to connect to (e.g., 'postgresql://user:password@localhost/dbname')."
    )

    parser.add_argument(
        '--models-module', 
        default='models', 
        help="Python module where the SQLAlchemy models are defined. Default is 'models'."
    )

    parser.add_argument(
        '--message', 
        default='Auto migration', 
        help="Message for the migration file. Only used with 'makemigrations'."
    )

    args = parser.parse_args()

    if args.command == 'makemigrations':
        run_makemigrations(
            alembic_config_path=args.alembic_config, 
            db_url=args.db_url, 
            models_module=args.models_module, 
            message=args.message
        )
    elif args.command == 'migrate':
        run_migrate(
            alembic_config_path=args.alembic_config, 
            db_url=args.db_url, 
            models_module=args.models_module
        )
    elif args.command == 'migrations':
        run_migrations(
            alembic_config_path=args.alembic_config, 
            db_url=args.db_url, 
            models_module=args.models_module
        )

if __name__ == "__main__":
    main()
