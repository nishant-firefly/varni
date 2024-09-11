# from ingestion import load_data_to_postgres
# from preprocessing import preprocess_data
# from model_training import train_supervised, train_unsupervised

# def run_pipeline():
#     # Step 1: Data Ingestion (using the tips dataset)
#     csv_file = 'data/tips.csv'  # File path from your system
#     db_url = 'postgresql://your_user:your_password@postgres/your_database'
#     load_data_to_postgres(csv_file, db_url)
    
#     # Step 2: Preprocess Data (customize the function for your dataset)
#     preprocess_data(db_url)
    
#     # Step 3: Model Training (both supervised and unsupervised models)
#     train_supervised(db_url)
#     train_unsupervised(db_url)

# if __name__ == "__main__":
#     run_pipeline()

from ingestion import load_data_to_postgres
from preprocessing import preprocess_data
from model_training import train_supervised, train_unsupervised

def run_pipeline():
    # Step 1: Data Ingestion
    csv_file = 'data/tips.csv'  # File path from your system
    db_url = 'postgresql://your_user:your_password@postgres/your_database'  # Ensure this matches your PostgreSQL config
    load_data_to_postgres(csv_file, db_url)
    
    # Step 2: Preprocess Data
    preprocess_data(db_url)
    
    # Step 3: Model Training
    train_supervised(db_url)
    train_unsupervised(db_url)
    
if __name__ == "__main__":
    run_pipeline()

