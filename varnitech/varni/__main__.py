import sys
from varni.dbs.migrations import varni_db_setup

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "initialize":
        # Execute the desired function from varni_db_setup
        varni_db_setup.main()
    else:
        print("Usage: python -m varni initialize")

if __name__ == "__main__":
    main()
