# Varni

Varni is a low-code/no-code platform proprietary to Varnitech.co. All rights reserved. This software cannot be used, modified, or distributed without explicit permission from Varnitech.co.

## Installation

### Install from GitHub (Production)

To install the Varni package directly from GitHub in a production environment, use the following command:

```$ pip install git+https://github.com/nishant-firefly/varni.git``` 

### Installation Mode : Development
``` git clone https://github.com/nishant-firefly/varni.git 
cd varni
pip install -e .
python -c "import varni.hello_world"
# Can change the hello world and verify its reflecting without reinstalling
```
### Fresh Setup Prject 
.env
``` 
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=your_database_name
MODEL_MODULES=varni.dbs.auth.models,example_project.models.custom_user
PROJECT_NAME=example_project
```


### Installation Mode : Development
``` git clone https://github.com/nishant-firefly/varni.git 
cd varni
pip install -e .
python -c "import varni.hello_world"
# Can change the hello world and verify its reflecting without reinstalling
```
# License
This software is proprietary to Varnitech.co. All rights are reserved. Unauthorized use, modification, or distribution of this software is strictly prohibited. For any inquiries regarding permissions, please contact nishant.saxena@varnitech.co.

## Author
Nishant Saxena  
nishant.saxena@varnitech.co



This version of the `README.md` has the author section formatted with your name and email address on separate lines.



