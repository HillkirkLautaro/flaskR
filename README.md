# Flaskr

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-green?logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![SQLite](https://img.shields.io/badge/SQLite-3.39-lightgrey?logo=sqlite&logoColor=blue)](https://www.sqlite.org/index.html)
[![Jinja](https://img.shields.io/badge/Jinja2-Red?logo=jinja&logoColor=white)](https://jinja.palletsprojects.com/)
[![Flask-Login](https://img.shields.io/badge/Flask--Login-Blue?logo=python&logoColor=white)](https://flask-login.readthedocs.io/en/latest/)
[![Flask-WTF](https://img.shields.io/badge/Flask--WTF-Orange?logo=python&logoColor=white)](https://flask-wtf.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## About

**Flaskr** is an open-source microblog web application built with Flask.  
It allows users to register, log in, and post short messages (up to 280 characters), similar to Twitter.  
The project is designed to be simple, modular, and educational, perfect as a learning tool or a foundation for further development.

---

## Features

- User registration, login, and logout  
- Create, view, and list posts  
- SQLite database with SQLAlchemy ORM  
- HTML templates with Jinja2  
- Form validation with Flask-WTF  
- User session management with Flask-Login  

---

## Installation

1. Clone the repository  
   ```bash
   git clone https://github.com/HillkirkLautaro/flask-tutorial.git
   cd flask-tutorial

2. Create a virtual environment and activate it  
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS and Linux

3. Install dependencies  
   ```bash
   pip install -r requirements.txt

4. Initialize the database  
   ```bash
   flask db init
   flask db migrate
   flask db upgrade

5. Run the application  
   ```bash
   flask run

---

## Usage

- Register a new user account  
- Log in and create posts  
- View and list posts  
- Log out

---

## License

MIT License

---

## Author

[Lautaro Hillkirk](https://www.linkedin.com/in/lautaro-hillkirk)

## Documentation

[![Documentation](https://docs.google.com/document/d/1cUACB4fodTx8NRdUF3NGW8TbXivWZn6bVH6xnfBgGtg/edit?tab=t.0)

---
