import psycopg2
import json

def lambda_handler(event, context):
    connection = psycopg2.connect(
        host="postgres_db",
        database="your_database",
        user="your_user",
        password="your_password"
    )
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM preprocessed_data LIMIT 10;")
    data = cursor.fetchall()
    
    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
