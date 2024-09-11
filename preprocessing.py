import pandas as pd
from sqlalchemy import create_engine

def preprocess_data(db_url):
    # Connect to the PostgreSQL database
    engine = create_engine(db_url)
    
    # Load data from the PostgreSQL table
    df = pd.read_sql('SELECT * FROM tips', engine)
    
    # Example preprocessing steps:
    
    # 1. Handle missing values (if any)
    df = df.dropna()
    
    # 2. Feature scaling (standardize 'total_bill' and 'tip')
    df[['total_bill', 'tip']] = (df[['total_bill', 'tip']] - df[['total_bill', 'tip']].mean()) / df[['total_bill', 'tip']].std()
    
    # 3. Encode categorical variables (e.g., 'sex', 'smoker', 'day', 'time')
    df = pd.get_dummies(df, columns=['sex', 'smoker', 'day', 'time'], drop_first=True)
    
    # Save the preprocessed data back to the database in a new table
    df.to_sql('preprocessed_tips', engine, if_exists='replace', index=False)
    print("Data preprocessing completed and saved!")

if __name__ == "__main__":
    db_url = 'postgresql://your_user:your_password@postgres/your_database'
    preprocess_data(db_url)
