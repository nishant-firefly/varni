# from sklearn.metrics import mean_squared_error, silhouette_score
# from sqlalchemy import create_engine
# import pandas as pd

# def evaluate_supervised(model, db_url):
#     # Fetch preprocessed data from the PostgreSQL database
#     engine = create_engine(db_url)
#     df = pd.read_sql('SELECT * FROM preprocessed_tips', engine)
    
#     # Features and target for evaluation
#     X = df[['total_bill']]
#     y_true = df['tip']
    
#     # Make predictions
#     y_pred = model.predict(X)
    
#     # Calculate mean squared error
#     mse = mean_squared_error(y_true, y_pred)
#     print(f"Supervised model evaluation: MSE = {mse}")

# def evaluate_unsupervised(model, db_url):
#     # Fetch preprocessed data from the PostgreSQL database
#     engine = create_engine(db_url)
#     df = pd.read_sql('SELECT * FROM preprocessed_tips', engine)
    
#     # Features for clustering
#     X = df[['total_bill', 'tip']]
    
#     # Get predicted cluster labels
#     cluster_labels = model.predict(X)
    
#     # Calculate silhouette score
#     silhouette_avg = silhouette_score(X, cluster_labels)
#     print(f"Unsupervised model evaluation: Silhouette Score = {silhouette_avg}")

# if __name__ == "__main__":
#     db_url = 'postgresql://your_user:your_password@postgres/your_database'
    
#     # Load trained models (dummy models for demonstration)
#     supervised_model = None  # Load your trained regression model here
#     unsupervised_model = None  # Load your trained clustering model here
    
#     evaluate_supervised(supervised_model, db_url)
#     evaluate_unsupervised(unsupervised_model, db_url)






import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, silhouette_score
from sklearn.cluster import KMeans
from joblib import dump, load

# Step 1: Load Preprocessed Data from PostgreSQL
def load_data(db_url):
    # Connect to PostgreSQL and load the preprocessed data
    engine = create_engine(db_url)
    df = pd.read_sql('SELECT * FROM preprocessed_tips', engine)  # Adjust table name if necessary
    return df

# Step 2: Split the data into features and target
def split_data(df):
    # Replace 'target' with the actual column name of your target variable
    X = df.drop(columns=['size'])  # Features
    y = df['size']  # Target variable
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

# Step 3: Train the Supervised Model
def train_supervised(X_train, y_train):
    model = LogisticRegression()  # Example supervised model (Logistic Regression)
    model.fit(X_train, y_train)
    dump(model, 'supervised_model.joblib')  # Save the trained model
    print("Supervised model trained and saved.")
    return model

# Step 4: Evaluate the Supervised Model
def evaluate_supervised(X_test, y_test):
    # Load the saved supervised model
    model = load('supervised_model.joblib')
    y_pred = model.predict(X_test)
    
    # Calculate accuracy and generate a classification report
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred)
    
    print(f'Accuracy: {accuracy}')
    print(f'Classification Report:\n{report}')

# Step 5: Train the Unsupervised Model
def train_unsupervised(X):
    model = KMeans(n_clusters=3)  # Example unsupervised model (KMeans with 3 clusters)
    model.fit(X)
    dump(model, 'unsupervised_model.joblib')  # Save the trained model
    print("Unsupervised model trained and saved.")
    return model

# Step 6: Evaluate the Unsupervised Model
def evaluate_unsupervised(X):
    # Load the saved unsupervised model
    model = load('unsupervised_model.joblib')
    labels = model.predict(X)
    
    # Calculate the silhouette score (used for clustering evaluation)
    score = silhouette_score(X, labels)
    
    print(f'Silhouette Score: {score}')

# Main Execution Block
if __name__ == "__main__":
    # Database URL
    db_url = 'postgresql://your_user:your_password@postgres/your_database'  # Replace with actual database URL
    
    # Step 1: Load preprocessed data from PostgreSQL
    df = load_data(db_url)
    
    # Step 2: Split data for supervised model
    X_train, X_test, y_train, y_test = split_data(df)
    
    # Step 3: Train and evaluate the supervised model
    train_supervised(X_train, y_train)
    evaluate_supervised(X_test, y_test)
    
    # Step 4: Train and evaluate the unsupervised model
    train_unsupervised(df)  # Using the entire dataset for unsupervised learning
    evaluate_unsupervised(df)
