Samodelkov Industries Analytics
About the Company

Samodelkov Industries is a data analytics company.
The project focuses on analyzing the customer database to understand customer distribution by regions, popular cities, and unique clients.

About the Project

This project performs basic analytics on the customers of Samodelkov Industries.

SQL queries are used to count customers by state, city, ZIP code, unique customers, and check for duplicates.

A Python script is provided to run the SQL queries automatically and save the results to CSV files.

Repository Structure
Samodelkov-Analytics/
│
├── customers_setup.sql         # Table creation and CSV import
├── queries.sql                 # 10 analytical SQL queries
├── main.py                     # Python script for running analytics
├── olist_customers_dataset2.csv  # CSV file with customer data
├── images/
│   └── analytics_screenshot.png  # Screenshot of analytics
└── README.md                   # This file

Analytics Screenshot

How to Run the Project
1. Create Table and Import CSV

Make sure PostgreSQL is installed and the database is created.

Open psql or pgAdmin.

Run the customers_setup.sql script:

\i 'C:\Users\Пользователь\Desktop\DATAVISUALISATION/customers_setup.sql'


✅ The customers table will be created and the CSV data imported.

2. Run SQL Analytics Queries

Open queries.sql in psql or pgAdmin.

Execute all 10 queries.

Results can be viewed in the terminal or in pgAdmin.

3. Run Python Script

Install the required Python libraries:

pip install psycopg2-binary pandas


Open main.py and configure your database connection:

DB_HOST = 'localhost'
DB_NAME = 'MAXIMVISUAL'
DB_USER = 'postgres'
DB_PASS = 'maxim22s2'
DB_PORT = 5433


Run the script:

python main.py


The script will display results in the terminal and save CSV files in the project folder.

Tools and Resources

PostgreSQL

psql / pgAdmin

Python 3.x

Python libraries: psycopg2-binary, pandas

Git & GitHub

Customer CSV file

VS Code / Notepad++ (for editing scripts)
