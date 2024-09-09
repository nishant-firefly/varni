import sys
from varni.dbs.migrations import varni_db_setup

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "initialize":
            # Execute the initialize function
            varni_db_setup.main()

        elif command == "create-db-docker":
            # Execute the create_docker_compose_yaml function
            varni_db_setup.setup_project_files()

        elif command == "syncdb":
            # Execute the main_alembic function
            varni_db_setup.main_alembic()

        else:
            print(f"Unknown command: {command}")
            print("Usage: python -m varni [initialize | create-db-docker | syncdb]")

    else:
        print("Usage: python -m varni [initialize | create-db-docker | syncdb]")

if __name__ == "__main__":
    main()
