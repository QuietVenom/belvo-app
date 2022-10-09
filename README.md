# belvo-app
This is a project to connect to the Belvo API using FastAPI

## Installation

Install python in your computer.
https://www.python.org/downloads/

Select or Create a folder or directory for this project and create a virtual enviroment to install all needed packages.

```bash
py -m venv venv
```

Activate the venv running the following command in the root directory where you created the venv.

```bash
venv/Scripts/activate
```

Run the following to deactivate.

```bash
deactivate
```

Please clone this project directly using git.
This project includes requirements.txt file tha you should use to install required packages to run this project.

```bash
pip install -r requirements.txt
```

Remember to set the correct python interpreter for your project.

To run this project you will need a postgres database. DBeaver is an easy option.
Create your database and prepare the following information:
postgresql://{user}:{password }@localhost:{PORT}/{database_name}

On your terminal with the currently active venv run the following

```bash
alembic init migrations
```

You will have a new alembic.ini file
Place the url postgresql://%(DB_USER)s:%(DB_PASSWORD)s@localhost:{PORT}/{database_name} in the sqlalchemy.url variable.

```python
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASSWORD)s@localhost:{PORT}/{database_name}
```

Inside the migrations folder you will find an env.py file. Open it and place the followig code.

```python
from decouple import config as env_config
from db import metadata
import models

...

section = config.config_ini_section
config.set_section_option(section, "DB_USER", env_config("DB_USER"))
config.set_section_option(section, "DB_PASSWORD", env_config("DB_PASSWORD"))

...

target_metadata = metadata

``` 

Finally you will create a .env file

```python
DB_USER={value}
DB_PASSWORD={value}
JWT_SECRET={value}
BELVO_ID={value}
BELVO_SECRET={value}
BELVO_URL=https://sandbox.belvo.com
```

Now we can create the table, run the following in your terminal.

```bash
alembic revision --autogenerate -m "Initial"
```

```bash
alembic upgrade head
```

This will be all for preparations.

## Usage

In the terminal, with the venv still active run the following command

```bash
uvicorn main:app --reload
```

and open the link

http://127.0.0.1:8000/docs

You will need to create a profile to log in. After creating a new profile of logging in with an existing profile, you wil get an authorization token to validate your access on the upper right side. Just copy and paste the token and select login.

Then you will be able to use some belvo endpoints through the swagger UI.
Using the last endpoint "run_dashboard" will create an example file of can be shown to the final client. Open the TEMP_FILES folder in your directory to find the newly created html file.

## License
[MIT](https://choosealicense.com/licenses/mit/)
