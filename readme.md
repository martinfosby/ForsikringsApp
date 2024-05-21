# BodoVision

## Overview
This project is a web application built using the Flask framework. It provides a simple and efficient way to save your real life insurances. The application includes features such as user authentication, database interaction, and crud operations.

## Features
- User registration and authentication
- CRUD operations on a database
- Responsive UI with HTML/CSS
- Integration with a mysql database via azure for production and sqlite for development.
- Register insurances, settlements and offers

## Installation

### Prerequisites
- Python 3.12.2 or lower
- pip (Python package installer)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/LC5466/BodoVision.git
   ```
   If you are having problems with http try using ssh, make sure you have ssh key first.
   ```bash
   git clone git@github.com:LC5466/BodoVision.git
   ```

2. **Create virtual environment and activate environment**
    Go to application folder: 
    ```bash
    cd BodoVision
    ```
    On Windows:
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
    On Unix:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install requirements via pip**
    inside bodovision folder run:
    ```bash
    pip install -r requirements.txt
    ```


## Usage
1. **Run the application**
    if you have vscode there is a .vscode file that you can use else you can run it with:

    ```bash
    cd flask_app
    flask run
    ```

    If you want to turn on debug:
    ```bash
    flask run --debug
    ```
2. **Access the application**
    Open your web browser and navigate to http://127.0.0.1:5000/.



## Flask Project Structure
```
flask_app/
├── app/
│   ├── blueprints/
│   │   ├── administrator/
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── auth/
│   │   │   ├── forms/
│   │   │   │   ├── change_password_form.py
│   │   │   │   ├── change_username_form.py
│   │   │   │   ├── delete_form.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── login_form.py
│   │   │   │   └── register_form.py
│   │   │   ├── __init__.py
│   │   │   ├── login_manager.py
│   │   │   └── views.py
│   │   ├── companies/
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── contacts/
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── insurances/
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── main/
│   │   │   ├── __init__.py
│   │   │   ├── static/
│   │   │   │   └── style.css
│   │   │   └── views.py
│   │   ├── offers/
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── settlements/
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   │   ├── unit_types/
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   └── views.py
│   ├── extensions.py
│   ├── __init__.py
│   ├── models/
│   │   ├── data.py
│   │   └── __init__.py
│   ├── templates/
│   │   ├── administrator/
│   │   │   └── home.html
│   │   ├── auth/
│   │   │   ├── change_password.html
│   │   │   ├── change_username.html
│   │   │   ├── delete.html
│   │   │   ├── detail.html
│   │   │   ├── list.html
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── base.html
│   │   ├── companies/
│   │   │   ├── companies_list.html
│   │   │   └── make_company.html
│   │   ├── contacts/
│   │   │   ├── contacts_list.html
│   │   │   └── make_contact.html
│   │   ├── insurances/
│   │   │   ├── delete_insurance.html
│   │   │   ├── insurances_list.html
│   │   │   └── make_insurance.html
│   │   ├── macros.html
│   │   ├── main/
│   │   │   └── index.html
│   │   ├── offers/
│   │   │   ├── delete_offer.html
│   │   │   ├── offers_list.html
│   │   │   └── register_offer.html
│   │   ├── settlements/
│   │   │   ├── delete_settlement.html
│   │   │   ├── make_settlement.html
│   │   │   └── settlements_list.html
│   │   ├── unit_types/
│   │   │   ├── make_unit_type.html
│   │   │   └── unit_types_list.html
│   └── utils.py
├── config.py
├── log_handler.py
├── res/
│   ├── __init__.py
│   └── strings_res.json
├── run.py
└── tests/
    ├── conftest.py
    ├── __init__.py
    └── test_app.py
└── requirements.txt
```


## Testing
To run unit tests:
```bash
cd BodoVision
pytest
```
If you have editor like vscode, you can setup a testing


## Database
For this application we used azure db as a development server, and also production server in the future. But you can use whatever relationship database you would like. This application uses a config file for easy setup of the database, be sure to arrange your database info in a .env file. These values are configured:

```
    DB_SERVER=?
    DATABASE=?
    USERNAME=?
    PASSWORD=?
```