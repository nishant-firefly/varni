import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sqlalchemy import create_engine

def train_supervised(db_url):
    # Fetch the tips data from Postgres
    engine = create_engine(db_url)
    df = pd.read_sql('SELECT * FROM tips', engine)
    
    # Assume `total_bill` as feature and `tip` as the target for regression
    X = df[['total_bill']]
    y = df['tip']
    
    # Train a simple Linear Regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Output results (for now, just print them)
    print(f"Regression Coefficients: {model.coef_}")
    print(f"Intercept: {model.intercept_}")

def train_unsupervised(db_url):
    # Fetch the tips data from Postgres
    engine = create_engine(db_url)
    df = pd.read_sql('SELECT * FROM tips', engine)
    
    # Use 'total_bill' and 'tip' as features for clustering
    X = df[['total_bill', 'tip']]
    
    # Train a simple KMeans model with 3 clusters
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)
    
    # Output the cluster centers
    print(f"Cluster Centers: {kmeans.cluster_centers_}")

if __name__ == "__main__":
    db_url = 'postgresql://your_user:your_password@postgres/your_database'
    train_supervised(db_url)
    train_unsupervised(db_url)
