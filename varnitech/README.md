## Branch: AWS MLOps pipeline steup

**OutLine:**
 To create an MLOps project using AWS services and deploy and invoke it with Docker Compose, you'll need to design a full pipeline that involves data ingestion, preprocessing, model training (both supervised and unsupervised), and deployment to AWS services, along with integrating a PostgreSQL database to handle CSV data. 

python -m venv venv
.\venv\Scripts\activate

pip install -r requirements.txt

## varify the installation
pip list

## for build the docker compose
(Run PostgreSQL and the MLOps Pipeline with Docker Compose)
Use Docker Compose to build and run both PostgreSQL and the MLOps pipeline:

docker-compose up --build

**for run the docker-compose**

docker-compose up -d

**for pipe line run**
docker logs mlops_app


**output:-------**

(venv) PS D:\mlops_project> docker logs mlops_app
Data loaded to PostgreSQL successfully!
Data preprocessing completed and saved!    
Regression Coefficients: [0.10502452]      
Intercept: 0.9202696135546731
Cluster Centers: [[36.71628571  4.602     ]
 [22.22193182  3.37988636]
 [13.11710744  2.2568595 ]]




## pipeline ran successfully! Here's a quick breakdown of what each log output indicates:** 

**Data loaded to PostgreSQL successfully!**

**Ingestion.py script successfully loaded the raw_data.csv into the PostgreSQL database.Data preprocessing completed and saved!**

**The preprocessing.py script completed the data cleaning and transformation steps (e.g., handling missing values, feature scaling, and encoding) and saved the processed data back into a new table in your PostgreSQL database.Regression Coefficients: [0.10502452] Intercept: 0.9202696135546731**

**This indicates that your supervised model (likely a linear regression model) has been trained successfully, and it is displaying the model's coefficients and intercept.Cluster Centers:

** Your unsupervised model (likely K-means clustering) has been trained, and the centers of the clusters have been printed. The cluster centers represent the centroids of the groups found in the data. **




** Check PostgreSQL: You can verify that the preprocessed data has been saved correctly by accessing the preprocessed_tips table in PostgreSQL. **

Since PostgreSQL is running inside a Docker container, you'll need to enter the container to access it.

## 1. Get the PostgreSQL container ID: Run the following command to list your running containers:

docker ps

## 2.Access the PostgreSQL container:

docker exec -it postgres_db bash

## Connect to the PostgreSQL database: 

psql -U your_user -d your_database


## Verify the Preprocessed Data

**List the tables:** Run this command to list all the tables in the database:
\dt


**Query the preprocessed_tips table:** Run the following SQL query to retrieve data from the preprocessed_tips table:

SELECT * FROM preprocessed_tips LIMIT 10;

## Output:

your_database=# \dt
               List of relations
 Schema |       Name        | Type  |   Owner
--------+-------------------+-------+-----------
 public | preprocessed_tips | table | your_user
 public | tips              | table | your_user
(2 rows)

your_database=# SELECT * FROM preprocessed_tips LIMIT 10;
      total_bill      |         tip         | size | Gender_Male | smoker_Yes | day_Sat | day_Sun | day_Thur | time_Lunch
----------------------+---------------------+------+----------+------------+---------+---------+----------+------------
 -0.31406574275923616 |  -1.436993214215838 |    2 | f        | f          | f       | t       | f        | f
  -1.0610543154877743 | -0.9672172242446297 |    3 | t        | f          | f       | t       | f        | f
  0.13749727413831675 |  0.3626101935200211 |    3 | t        | f          | f       | t       | f        | f
   0.4374159943165417 | 0.22529105798997567 |    2 | t        | f          | f       | t       | f        | f
   0.5396354832162364 |  0.4421107456689947 |    4 | f        | f          | f       | t       | f        | f
   0.6182658592929247 |  1.2371162671587317 |    4 | t        | f          | f       | t       | f        | f
   -1.237411016116918 | -0.7214882448750747 |    2 | t        | f          | f       | t       | f        | f
   0.7968691420956879 | 0.08797192245993025 |    4 | t        | f          | f       | t       | f        | f
  -0.5331075046871533 | -0.7503975365656106 |    2 | t        | f          | f       | t       | f        | f
   -0.562313072944209 | 0.16747247460890385 |    2 | t        | f          | f       | t       | f        | f
(10 rows)

**Exit PostgreSQL:**
\q

**Exit the container:**
exit

## Running the Evaluation
docker-compose run app /bin/bash
python app/evaluation.py

**Output**
Supervised model trained and saved.
/usr/local/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1531: UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, f"{metric.capitalize()} is", len(result))
/usr/local/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1531: UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, f"{metric.capitalize()} is", len(result))
/usr/local/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1531: UndefinedMetricWarning: Precision is ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
  _warn_prf(average, modifier, f"{metric.capitalize()} is", len(result))
Accuracy: 0.6326530612244898
Classification Report:
              precision    recall  f1-score   support

           1       0.00      0.00      0.00         2
           2       0.67      1.00      0.80        30
           3       0.00      0.00      0.00         8
           4       0.25      0.14      0.18         7
           5       0.00      0.00      0.00         1
           6       0.00      0.00      0.00         1

    accuracy                           0.63        49
   macro avg       0.15      0.19      0.16        49
weighted avg       0.44      0.63      0.52        49

Unsupervised model trained and saved.
Silhouette Score: 0.1875602597290981


