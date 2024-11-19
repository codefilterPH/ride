# Django Project Setup Guide

This guide provides the steps to set up and run the Django project with all necessary dependencies and configurations.

## Step 1: Set Up Python and Virtual Environment

### 1.1 Install Python

Make sure Python 3.8 or later is installed on your system. You can download the latest version from [python.org](https://www.python.org/downloads/).

To check if Python is installed, run:

```
python --version
```

### Create a virtual environment
```python -m venv venv```

### Activate the virtual environment
#### On Windows:
```venv\Scripts\activate```

#### On macOS/Linux:
source venv/bin/activate

### 2.1 Install Required Packages
With your virtual environment activated, run the following command to install the dependencies listed in requirements.txt:
<br>```pip install -r requirements.txt```


## Step 3: Set Up Environment Variables
### 3.1 Create secrets Directory and .env File
Create a directory named secrets in the root of your project and create a .env file inside the directory to store environment variables.

#### Create a secrets directory
```mkdir secrets```

#### Create a .env file inside the secrets directory
```touch secrets/.env```

### 3.2 Set Environment Variables
Open the .env file in your text editor and add the following environment variables:

#### Django settings
```
export SECRET_KEY='django-insecure-=m7w#m$flq)ssl2=#ri*b#d)+bd(+8hgo2$3cv%%ywu=#71p)z'
export DEBUG=True
export ALLOWED_HOSTS=localhost,127.0.0.1,server.mshome.net
```
#### JWT settings
```export JWT_SECRET_KEY="RidesPassword!@#123"```

### 3.3 Load Environment Variables
To load the environment variables from the .env file, you can use the dotenv package, which will automatically read and load the values. Make sure that the package is installed by adding python-dotenv to requirements.txt. Then, in your Django settings.py, add the following code at the top:
```
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(BASE_DIR, 'secrets', '.env'))

# Retrieve the environment variables
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
```
This will load the environment variables into the Django settings.

## Step 4: Run Django Management Commands
### 4.1 Run Migrations
Make sure your database is up to date with the latest migrations:
#### Create migrations based on changes in models
```python manage.py makemigrations```

#### Apply the migrations to the database
```python manage.py migrate```

### 4.2 Create Superuser
To create a superuser for accessing the Django Admin interface, run the following command:
```python manage.py createsuperuser```
This will prompt you to enter a username, email, and password for the superuser account.

### 4.3 Create Regular User
You can also create a regular user via the following command:
```python manage.py createregularuser```

### 4.4 Run the Development Server
Finally, start the Django development server:
```python manage.py runserver```
The application should now be accessible at http://127.0.0.1:8000.

## Step 5: Access the Admin Panel
Visit the Django Admin panel at the following URL:
```http://127.0.0.1:8000/admin/```

Log in with the superuser credentials you created earlier.
