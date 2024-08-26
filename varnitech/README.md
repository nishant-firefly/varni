# Instructions 
``cd varni
pip install -e .
python -c "import varni; varni.how_to_setup()" 


## TODO make it a command 
python ..\varnitech\varni\dbs\migrations\varni_db_setup.py

## After projectc created above :
```cd example_project```

example_project/
├── models/
│   ├── __init__.py          # Import and expose your models here
│   └── custom_user.py       # Define your models in individual files
└── manage.py                # Created during setup



            ├── aut_models.py.template
            ├── example_model.py.template
            └── README.txt.template

python manage.py makemigrations

python manage.py migrate

python manage.py rollback


```
varni.how_to