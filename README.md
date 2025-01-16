# python-flask-api-streamlit
Python project using Flask for API connected to MySQL and uses Streamlit for UI

project contains 2 files:

app.py:
The main controller with all APIs and SQL connection
Note: add your SQL credentials in this file before running

ui.py:
contains Streamlit code for UI and calls the APIs using user inputted values

Steps to run:

1) Add you MySql credentials to app.py
2) pip install flask mysql-connector-python streamlit pandas
3) open 2 terminals
4) in 1st terminal : python app.py
5) in 2nd terminal : streamlit run ui.py OR python -m streamlit run ui.py


It should open the UI in the browser automatically

