import pandas as pd
from sqlalchemy import create_engine

def load_data_to_postgres(csv_file, db_url):
    # Load data from the specified CSV file
    df = pd.read_csv(csv_file)
    
    # Connect to PostgreSQL database
    engine = create_engine(db_url)
    
    # Load data into PostgreSQL table
    df.to_sql('tips', engine, if_exists='replace', index=False)
    print("Data loaded to PostgreSQL successfully!")

if __name__ == "__main__":
    # Updated file path for your CSV file
    csv_file = 'data/tips.csv'
    # PostgreSQL connection URL
    db_url = 'postgresql://your_user:your_password@postgres/your_database'
    
    load_data_to_postgres(csv_file, db_url)
